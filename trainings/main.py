"""Requests handlers."""
import time
import logging

from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.applications import get_swagger_ui_html
from environ import to_config
from newrelic.agent import (
    record_custom_metric as record_metric,
    register_application,
)
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from httpx import Client

from trainings.authorization import assert_can_create_training, get_permissions
from trainings.config import AppConfig
from trainings.database.url import get_database_url
from trainings.database.models import Base
from trainings.database.hydrator import hydrate as hydrate_model
from trainings.database.data import init_db
from trainings.request.helper import (
    read_training,
    read_user,
    read_rating,
)
from trainings.healthcheck import HealthCheckDto
from trainings.trainings.dto import (
    TrainingIn,
    TrainingOut,
    TrainingPatch,
    TrainingsWithPagination,
    TrainingFilters,
)
from trainings.trainings.dao import browse, add, edit
from trainings.trainings.non_bread_queries import (
    get_count as get_training_count
)
from trainings.trainings.helper import get_columns_and_values
from trainings.trainings.hydrator import hydrate as hydrate_dto
from trainings.training_types.dto import TrainingTypesOut
from trainings.training_types.dao import browse as browse_types
from trainings.training_types.hydrator import hydrate as hydrate_training_types
from trainings.exercises.dto import ExercisesOut
from trainings.exercises.dao import browse as browse_exercises
from trainings.exercises.hydrator import hydrate as hydrate_exercises
from trainings.firebase import save
from trainings.user_trainings.dto import UserTrainingIn
from trainings.user_trainings.dao import (
    add as add_user_training,
    browse as browse_user_trainings,
    delete as delete_user_training,
)
from trainings.user_trainings.non_bread_queries import (
    get_count as get_favourite_trainings_count
)
from trainings.rating.dto import TrainingRating
from trainings.rating.dao import add as add_rating

BASE_URI = "/trainings"
TYPES_URI = BASE_URI + "/types/"
EXERCISES_URI = BASE_URI + "/exercises/"
USER_TRAININGS_URI = "/users/{user_id}/trainings"
DOCUMENTATION_URI = BASE_URI + "/documentation/"
TRAINING_ID = "/{training_id}"
USER_TRAINING_URI = USER_TRAININGS_URI + TRAINING_ID
CONFIGURATION = to_config(AppConfig)
START = time.time()
NR_APP = register_application()
COUNTER = {"count": 1}

app = FastAPI(
    debug=CONFIGURATION.log_level.upper() == "DEBUG",
    openapi_url=DOCUMENTATION_URI + "openapi.json"
)
METHODS = [
    "GET",
    "get",
    "POST",
    "post",
    "PUT",
    "put",
    "PATCH",
    "patch",
    "OPTIONS",
    "options",
    "DELETE",
    "delete",
    "HEAD",
    "head",
]
ORIGIN_REGEX = "(http)?(s)?(://)?(.*vercel.app|localhost|local)(:3000)?.*"
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=ORIGIN_REGEX,
    allow_credentials=True,
    allow_methods=METHODS,
    allow_headers=['*']
)

logging.basicConfig(encoding="utf-8", level=CONFIGURATION.log_level.upper())

ENGINE = create_engine(
    get_database_url(CONFIGURATION),
    connect_args={"sslmode": "require" if CONFIGURATION.db.ssl else "disable"},
    pool_pre_ping=True,
)


def get_db() -> Session:
    """Create a session."""
    return Session(autocommit=False, autoflush=False, bind=ENGINE)


if CONFIGURATION.db.create_structures:
    Base.metadata.create_all(bind=ENGINE)
    init_db(get_db())


# pylint: disable=too-many-arguments
@app.get(
    BASE_URI,
    response_model=TrainingsWithPagination,
    response_model_exclude_none=True,
)
async def get_trainings(
    trainer_id: str | None = None,
    training_type: str | None = None,
    difficulty: str | None = None,
    title: str | None = None,
    offset: int = 0,
    limit: int = 10,
    session: Session = Depends(get_db)
) -> TrainingsWithPagination:
    """Get trainings matching a filtering criteria."""
    record_metric('Custom/trainings/get', COUNTER, NR_APP)
    filters = TrainingFilters(
        trainer_id=trainer_id,
        type=training_type,
        difficulty=difficulty,
        title=title,
        offset=offset,
        limit=limit,
    )
    logging.info("Searching for trainings matching (%s)...", filters.dict())
    with session as open_session:
        trainings = browse(open_session, filters)
        count = get_training_count(open_session, filters)
    dtos = []
    logging.info("Building DTOs...")
    for training in trainings:
        dtos.append(hydrate_dto(training, CONFIGURATION))
    response = TrainingsWithPagination(
        items=dtos,
        offset=filters.offset,
        limit=filters.limit,
        count=count,
    )
    return response


@app.get(
    BASE_URI + "/{training_id}",
    response_model=TrainingOut,
    response_model_exclude_none=True,
    status_code=201,
)
async def get_training(
    training_id: int,
    session: Session = Depends(get_db)
) -> TrainingOut:
    """Get one training."""
    record_metric('Custom/trainings-id/get', COUNTER, NR_APP)
    with session as open_session:
        training = read_training(open_session, training_id)
    logging.info("Building DTO...")
    return hydrate_dto(training, CONFIGURATION)


@app.patch(
    BASE_URI + "/{training_id}",
    status_code=204,
)
async def modify_training(
    training_id: int,
    body: TrainingPatch,
    session: Session = Depends(get_db),
):
    """Modify one training."""
    record_metric('Custom/trainings-id/patch', COUNTER, NR_APP)
    logging.info("Received values (%s) to update.", body.dict())
    with session as open_session:
        logging.info("Searching for training...")
        training = read_training(open_session, training_id)
        logging.debug("Building values for query...")
        columns_and_values = get_columns_and_values(body)
        if "media" in columns_and_values:
            logging.info("Saving media...")
            columns_and_values["media"] = save(
                columns_and_values["media"],
                training.trainer_id,
                CONFIGURATION
            )
        logging.info(
            "Updating values (%s) of %s.", columns_and_values, training_id
        )
        edit(open_session, training_id, columns_and_values)


@app.post(
    BASE_URI,
    response_model=TrainingOut,
    response_model_exclude_none=True,
)
async def create_training(
    request: Request,
    training_to_create: TrainingIn,
    session: Session = Depends(get_db)
) -> TrainingOut:
    """Create a training."""
    if CONFIGURATION.auth.validate_credentials:
        logging.info("Validating permissions. Headers: %s", request.headers)
        permissions = get_permissions(request.headers, Client(), CONFIGURATION)
        assert_can_create_training(permissions)
    if training_to_create.media:
        logging.info("Saving media...")
        training_to_create.media = save(
            training_to_create.media,
            training_to_create.trainer_id,
            CONFIGURATION
        )
    logging.info("Creating training %s", training_to_create.dict())
    record_metric('Custom/trainings/post', COUNTER, NR_APP)
    with session as open_session:
        created_training = add(
            open_session, hydrate_model(open_session, training_to_create)
        )
    return hydrate_dto(created_training, CONFIGURATION)


@app.get(TYPES_URI, response_model=TrainingTypesOut)
async def get_types(session: Session = Depends(get_db)) -> TrainingTypesOut:
    """Get training types."""
    record_metric('Custom/trainings-types/get', COUNTER, NR_APP)
    logging.info("Searching for training types...")
    training_types = []
    with session as open_session:
        training_types = browse_types(open_session)
    logging.info("Building DTOs...")
    return hydrate_training_types(training_types)


@app.get(
    EXERCISES_URI,
    response_model=ExercisesOut,
    response_model_exclude_none=True,
)
async def get_exercises(session: Session = Depends(get_db)) -> ExercisesOut:
    """Get training exercises."""
    record_metric('Custom/trainings-exercises/get', COUNTER, NR_APP)
    logging.info("Searching for exercises...")
    exercises = []
    with session as open_session:
        exercises = browse_exercises(open_session)
    logging.info("Building DTOs...")
    return hydrate_exercises(exercises)


@app.post(USER_TRAININGS_URI, status_code=204)
async def save_training_for_user(
    user_id: str,
    training: UserTrainingIn,
    session: Session = Depends(get_db),
) -> None:
    """Save a training in user favourites."""
    logging.info(
        "Saving training %s for user %s...", training.training_id, user_id
    )
    record_metric('Custom/users-id-trainings/post', COUNTER, NR_APP)
    with session as open_session:
        read_training(open_session, training.training_id)
        read_user(open_session, user_id)
        try:
            add_user_training(open_session, user_id, training.training_id)
        except IntegrityError as exc:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="You already have that training as favourite."
            ) from exc


@app.delete(USER_TRAINING_URI, status_code=204)
async def delete_training_for_user(
    user_id: str,
    training_id: int,
    session: Session = Depends(get_db),
) -> None:
    """Delete a training in user favourites."""
    logging.info("Deleting training %s for user %s...", training_id, user_id)
    record_metric('Custom/users-id-trainings-id/delete', COUNTER, NR_APP)
    with session as open_session:
        read_training(open_session, training_id)
        read_user(open_session, user_id)
        delete_user_training(open_session, user_id, training_id)


@app.put(USER_TRAINING_URI, status_code=204)
async def rate_training(
    user_id: str,
    training_id: str,
    rating: TrainingRating,
    session: Session = Depends(get_db),
) -> None:
    """Rate a training."""
    logging.info(
        "User %s rates training %s with %s", user_id, training_id, rating.rate
    )
    record_metric('Custom/users-id-trainings-id/put', COUNTER, NR_APP)
    with session as open_session:
        read_user(open_session, user_id)
        read_training(open_session, training_id)
        add_rating(open_session, user_id, training_id, rating.rate)


@app.get(
    USER_TRAINING_URI + "/rating",
    response_model=TrainingRating,
)
async def get_user_rate_for_training(
    user_id: str,
    training_id: str,
    session: Session = Depends(get_db),
) -> TrainingRating:
    """Get a training rating by a user."""
    logging.info("Getting training %s rate by user %s", user_id, training_id)
    record_metric('Custom/users-id-trainings-id-rating/get', COUNTER, NR_APP)
    with session as open_session:
        read_user(open_session, user_id)
        read_training(open_session, training_id)
        rating = read_rating(open_session, user_id, training_id)
    return TrainingRating(rate=rating.rating)


@app.get(
    USER_TRAININGS_URI,
    response_model=TrainingsWithPagination,
    response_model_exclude_none=True,
)
async def get_favourite_training_for_user(
    user_id: str,
    offset: int = 0,
    limit: int = 10,
    session: Session = Depends(get_db),
) -> TrainingsWithPagination:
    """Return a user favourite trainings."""
    logging.info("Getting trainings for user %s...", user_id)
    record_metric('Custom/users-id-trainings/get', COUNTER, NR_APP)
    with session as open_session:
        read_user(open_session, user_id)
        # The following returns a Users database model with it's favourite
        # trainings.
        user = browse_user_trainings(open_session, user_id, offset, limit)
        count = get_favourite_trainings_count(open_session, user_id)
    dtos = []
    logging.info("Building DTOs...")
    for user_trainings in user.trainings:
        logging.debug("Building DTO of %s...", user_trainings.__dict__)
        dtos.append(hydrate_dto(user_trainings.training, CONFIGURATION))
    return TrainingsWithPagination(
        items=dtos,
        offset=offset,
        limit=limit,
        count=count,
    )


@app.get(BASE_URI + "/healthcheck/")
async def health_check() -> HealthCheckDto:
    """Check for how long has the service been running."""
    return HealthCheckDto(uptime=time.time() - START)


@app.get(DOCUMENTATION_URI, include_in_schema=False)
async def custom_swagger_ui_html(req: Request):
    """To show Swagger with API documentation."""
    root_path = req.scope.get("root_path", "").rstrip("/")
    openapi_url = root_path + app.openapi_url
    return get_swagger_ui_html(
        openapi_url=openapi_url,
        title="FIUFIT Trainings",
    )
