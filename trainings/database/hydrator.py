"""Hydrate database model objects from DTOs."""
import logging
from sqlalchemy.orm import Session

from trainings.database.models import (
    Difficulty,
    Exercise,
    Training,
    TrainingExercise,
    TrainingType,
)
from trainings.trainings.dto import TrainingIn


def hydrate(session: Session, training: TrainingIn) -> Training:
    """Create a database model object from a HTTP API DTO."""
    exercises = []
    logging.info("Building exercises for training...")
    for training_exercise in training.exercises:
        logging.debug(
            "Building exercise", **training_exercise.dict()
        )
        exercises.append(
            TrainingExercise(
                exercise=session.query(Exercise).filter(
                    Exercise.name == training_exercise.name,
                    Exercise.unit == training_exercise.unit
                ).one(),
                count=training_exercise.count,
                series=training_exercise.series
            )
        )
    logging.info("Building training...")
    foreign_keys = {
        "exercises": exercises,
        "type": session.query(TrainingType).filter(
            TrainingType.name == training.type
        ).one(),
        "difficulty": session.query(Difficulty).filter(
            Difficulty.name == training.difficulty
        ).one(),
    }
    fields = training.dict() | foreign_keys
    logging.debug("Exercise built", **fields)
    return Training(**fields)
