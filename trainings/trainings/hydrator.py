"""Hydrate DTOs from database objects."""
import logging
from trainings.config import AppConfig
from trainings.database.models import Training
from trainings.firebase import read
from trainings.trainings.dto import (Exercise, TrainingOut)


def hydrate(training: Training, config: AppConfig) -> TrainingOut:
    """Create an HTTP DTO from a model object."""
    logging.debug("Creating DTO for %s", training)
    media = None
    if training.media:
        media = read(str(training.media), config)
    dto = TrainingOut(
        id=int(training.id),
        trainer_id=str(training.trainer_id),
        tittle=str(training.tittle),
        description=str(training.description),
        difficulty=str(training.difficulty.name),
        type=str(training.type.name),
        media=media,
        blocked=bool(training.blocked),
        rating=0,
        exercises=[],
    )
    logging.info("Creating DTO for training exercises...")
    for exercise in training.exercises:
        logging.debug("Creating DTO for %s", exercise)
        dto.exercises.append(
            Exercise(
                name=str(exercise.exercise.name),
                type=str(exercise.exercise.type.name),
                unit=exercise.exercise.unit,
                count=exercise.count,
                series=exercise.series,
            )
        )
    return dto
