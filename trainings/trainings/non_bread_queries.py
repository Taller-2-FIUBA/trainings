"""Helper queries for trainings."""
import logging

from sqlalchemy.orm import Session
from trainings.database.models import Training
from trainings.trainings.dto import TrainingFilters
from trainings.trainings.helper import get_criteria


def get_count(session: Session, filters: TrainingFilters) -> int:
    """Return how many trainings match filters."""
    logging.info("Running count query...")
    return session.query(Training).filter(*get_criteria(session, filters))\
        .count()
