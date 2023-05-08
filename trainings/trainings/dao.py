"""DAO with B.R.E.A.D. functions for trainings."""
import logging

from sqlalchemy.orm import Session
from trainings.database.models import Training
from trainings.trainings.dto import TrainingFilters
from trainings.trainings.filters import get_criteria


def browse(session: Session, filters: TrainingFilters):
    """Return all trainings matching filters."""
    logging.info("Running query...")
    return session.query(Training).filter(*get_criteria(session, filters))\
        .offset(filters.offset).limit(filters.limit).all()


def read(session: Session, training_id: int) -> Training:
    """Return one training filtering by fields."""
    return session.query(Training).filter(
        Training.id == training_id,
    ).one()


def add(session: Session, training: Training) -> Training:
    """Create a training."""
    logging.info("Saving training...")
    session.add(training)
    session.commit()
    session.refresh(training)
    return training
