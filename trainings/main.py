"""Requests handlers."""
import logging

from fastapi import Depends, FastAPI
from environ import to_config
from prometheus_client import start_http_server
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

import trainings.metrics as m
from trainings.config import AppConfig
from trainings.database.url import get_database_url
from trainings.database.models import Base
from trainings.database.hydrator import hydrate as hydrate_model
from trainings.schemas import (
    TrainingIn,
    TrainingOut,
    TrainingsWithPagination,
    TrainingFilters,
)
from trainings.dao import browse, add, read
from trainings.hydrator import hydrate as hydrate_dto
from trainings.types.dto import TrainingTypesOut
from trainings.types.dao import browse as browse_types
from trainings.types.hydrator import hydrate as hydrate_training_types

BASE_URI = "/trainings"
TYPES_URI = BASE_URI + "/types/"
CONFIGURATION = to_config(AppConfig)
app = FastAPI(
    docs_url=BASE_URI + "/documentation",
    debug=CONFIGURATION.log_level.upper() == "DEBUG"
)

start_http_server(CONFIGURATION.prometheus_port)
logging.basicConfig(encoding='utf-8', level=CONFIGURATION.log_level.upper())


ENGINE = create_engine(get_database_url(CONFIGURATION))
if CONFIGURATION.db.create_structures:
    Base.metadata.create_all(bind=ENGINE)


def get_db() -> Session:
    """Create a session."""
    return Session(autocommit=False, autoflush=False, bind=ENGINE)


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
)
async def get_training(
    training_id: int,
    session: Session = Depends(get_db)
) -> TrainingsWithPagination:
    """Get one training."""
    m.REQUEST_COUNTER.labels(BASE_URI, "get").inc()
    logging.info("Searching for training %d...", training_id)
    with session as open_session:
        training = read(open_session, training_id)
    logging.info("Building DTO...")
    return hydrate_dto(training)


@app.post(
    BASE_URI,
    response_model=TrainingOut,
    response_model_exclude_none=True,
)
async def create_training(
    training_to_create: TrainingIn,
    session: Session = Depends(get_db)
) -> TrainingOut:
    """Create a training."""
    logging.info("Creating training", **training_to_create.dict())
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
