"""DAO with B.R.E.A.D. functions for trainings."""
import logging

from sqlalchemy.orm import Session
from trainings.database.models import Difficulty, Training, TrainingType
from trainings.trainings.dto import TrainingFilters


def browse(session: Session, filters: TrainingFilters):
    """Return all trainings matching filters."""
    criteria = []
    if filters.trainer_id:
        criteria.append(Training.trainer_id == filters.trainer_id)
    if filters.type:
        criteria.append(
            Training.type == session.query(TrainingType).filter(
                TrainingType.name == filters.type,
            ).one()
        )
    if filters.difficulty:
        criteria.append(
            Training.difficulty == session.query(Difficulty).filter(
                Difficulty.name == filters.difficulty,
            ).one()
        )
    logging.info("Running query...")
    return session.query(Training).filter(*criteria)\
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
