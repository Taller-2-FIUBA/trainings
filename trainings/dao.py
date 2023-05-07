"""DAO with B.R.E.A.D. functions for trainings."""
import logging

from sqlalchemy.orm import Session
from trainings.database.models import Training


def browse(session: Session, offset: int, limit: int):
    """Return all trainings."""
    return session.query(Training).offset(offset).limit(limit).all()


def add(session: Session, training: Training) -> Training:
    """Create a training."""
    logging.info("Saving training...")
    session.add(training)
    session.commit()
    session.refresh(training)
    return training
