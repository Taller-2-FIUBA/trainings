"""DAO functions for training types."""
import logging

from sqlalchemy.orm import Session
from trainings.database.models import TrainingType


def browse(session: Session):
    """Return all trainings types."""
    logging.info("Running query...")
    return session.query(TrainingType).all()
