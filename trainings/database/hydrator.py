"""Hydrate DTOs from database objects."""
import logging
from trainings.database.models import Training
from trainings.schemas import (Exercise, TrainingOut)


def hydrate(training: Training) -> TrainingOut:
    """Create an HTTP DTO from a model object."""
    logging.debug("Creating DTO for %s", training)
    dto = TrainingOut(
        id=int(training.id),
        trainer_id=str(training.trainer_id),
        tittle=str(training.tittle),
        description=str(training.description),
        difficulty=str(training.difficulty.name),
        type=str(training.type.name),
        media=str(training.media),
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
                unit=str(exercise.exercise.unit),
                count=exercise.count,
                series=exercise.series,
            )
        )
    return dto
