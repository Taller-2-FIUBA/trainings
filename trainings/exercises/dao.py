"""DAO functions for training exercises."""
import logging

from sqlalchemy.orm import Session
from trainings.database.models import Exercise


def browse(session: Session):
    """Return all trainings exercises."""
    logging.info("Running query...")
    return session.query(Exercise).all()
