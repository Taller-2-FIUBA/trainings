"""Requests handlers."""
import logging

from fastapi import Depends, FastAPI, HTTPException, Request
from environ import to_config
from prometheus_client import start_http_server
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from httpx import Client
from trainings.database.data import init_db

import trainings.metrics as m
from trainings.authorization import assert_can_create_training, get_permissions
from trainings.config import AppConfig
from trainings.database.url import get_database_url
from trainings.database.models import Base
from trainings.database.hydrator import hydrate as hydrate_model
from trainings.trainings.dto import (
    TrainingIn,
    TrainingOut,
    TrainingPatch,
    TrainingsWithPagination,
    TrainingFilters,
)
from trainings.trainings.dao import browse, add, edit, read
from trainings.trainings.hydrator import hydrate as hydrate_dto
from trainings.training_types.dto import TrainingTypesOut
from trainings.training_types.dao import browse as browse_types
from trainings.training_types.hydrator import hydrate as hydrate_training_types
from trainings.exercises.dto import ExercisesOut
from trainings.exercises.dao import browse as browse_exercises
from trainings.exercises.hydrator import hydrate as hydrate_exercises
from trainings.firebase import save

BASE_URI = "/trainings"
TYPES_URI = BASE_URI + "/types/"
EXERCISES_URI = BASE_URI + "/exercises/"
CONFIGURATION = to_config(AppConfig)
app = FastAPI(
    docs_url=BASE_URI + "/documentation",
    debug=CONFIGURATION.log_level.upper() == "DEBUG"
)

start_http_server(CONFIGURATION.prometheus_port)
logging.basicConfig(encoding="utf-8", level=CONFIGURATION.log_level.upper())

ENGINE = create_engine(
    get_database_url(CONFIGURATION),
    connect_args={"sslmode": "require"},
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
    offset: int = 0,
    limit: int = 10,
    session: Session = Depends(get_db)
) -> TrainingsWithPagination:
    """Get trainings matching a filtering criteria."""
    m.REQUEST_COUNTER.labels(BASE_URI, "get").inc()
    filters = TrainingFilters(
        trainer_id=trainer_id,
        type=training_type,
        difficulty=difficulty,
        offset=offset,
        limit=limit,
    )
    logging.info("Searching for trainings matching (%s)...", filters.dict())
    with session as open_session:
        trainings = browse(open_session, filters)
    dtos = []
    logging.info("Building DTOs...")
    for training in trainings:
        dtos.append(hydrate_dto(training))
    response = TrainingsWithPagination(
        items=dtos,
        offset=filters.offset,
        limit=filters.limit,
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
) -> TrainingsWithPagination:
    """Get one training."""
    m.REQUEST_COUNTER.labels(BASE_URI, "get").inc()
    logging.info("Searching for training %d...", training_id)
    try:
        with session as open_session:
            training = read(open_session, training_id)
    except NoResultFound as error:
        raise HTTPException(
            detail="Training not found.", status_code=404
        ) from error
    logging.info("Building DTO...")
    return hydrate_dto(training)


@app.patch(
    BASE_URI + "/{training_id}",
    status_code=204,
)
async def modify_training(
    training_id: int,
    values_to_update: TrainingPatch,
    session: Session = Depends(get_db),
):
    """Modify one training."""
    m.REQUEST_COUNTER.labels(BASE_URI, "patch").inc()
    columns_and_values = values_to_update.dict()
    logging.info(
        "Updating values (%s) of training %d...",
        columns_and_values,
        training_id
    )
    with session as open_session:
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
    logging.info("Validating permissions. Headers: %s", request.headers)
    permissions = get_permissions(request.headers, Client(), CONFIGURATION)
    assert_can_create_training(permissions)
    logging.info("Saving media...")
    training_to_create.media = save(training_to_create.media)
    logging.info("Creating training %s", training_to_create.dict())
    m.REQUEST_COUNTER.labels(BASE_URI, "post").inc()
    with session as open_session:
        created_training = add(
            open_session, hydrate_model(open_session, training_to_create)
        )
    return hydrate_dto(created_training)


@app.get(TYPES_URI, response_model=TrainingTypesOut)
async def get_types(session: Session = Depends(get_db)) -> TrainingTypesOut:
    """Get training types."""
    m.REQUEST_COUNTER.labels(TYPES_URI, "get").inc()
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
    m.REQUEST_COUNTER.labels(EXERCISES_URI, "get").inc()
    logging.info("Searching for exercises...")
    exercises = []
    with session as open_session:
        exercises = browse_exercises(open_session)
    logging.info("Building DTOs...")
    return hydrate_exercises(exercises)
