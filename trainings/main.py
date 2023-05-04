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
from trainings.schemas import TrainingsWithPagination
from trainings.dao import browse
from trainings.database.hydrator import hydrate

BASE_URI = "/trainings"
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


@app.get(BASE_URI, response_model=TrainingsWithPagination)
async def get_trainings(
    offset: int = 0,
    limit: int = 10,
    session: Session = Depends(get_db)
) -> TrainingsWithPagination:
    """Get all sessions."""
    m.REQUEST_COUNTER.labels(BASE_URI, "get").inc()
    logging.info("Running query...")
    with session as open_session:
        trainings = browse(open_session, offset, limit)
    dtos = []
    logging.info("Building DTOs...")
    for training in trainings:
        dtos.append(hydrate(training))
    response = TrainingsWithPagination(
        items=dtos,
        offset=offset,
        limit=limit
    )
    return response
