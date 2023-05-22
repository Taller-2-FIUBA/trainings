"""DAO with B.R.E.A.D. functions for trainings."""
import logging
from typing import Any, Dict

from sqlalchemy.orm import Session
from trainings.database.models import Training
from trainings.trainings.dto import TrainingFilters
from trainings.trainings.helper import get_criteria


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


def edit(session: Session, training_id: int, fields_to_update: Dict[str, Any]):
    """Update fields in a training."""
    logging.info("Running update query...")
    session.query(Training)\
        .filter(Training.id == training_id)\
        .update(values=fields_to_update)
    session.commit()


def add(session: Session, training: Training) -> Training:
    """Create a training."""
    logging.info("Saving training...")
    session.add(training)
    session.commit()
    session.refresh(training)
    return training
