"""Hydrate database model objects from DTOs."""
import logging
from fastapi import HTTPException, status
from sqlalchemy.orm.exc import NoResultFound
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
            "Building exercise %s", training_exercise.dict()
        )
        try:
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
        except NoResultFound as error:
            detail = "Could not save training. Exercise "\
                f"{training_exercise.name} {training_exercise.unit} not found."
            logging.warning(detail)
            raise HTTPException(
                detail=detail, status_code=status.HTTP_404_NOT_FOUND
            ) from error
    logging.info("Building training...")
    try:
        training_type = session.query(TrainingType).filter(
            TrainingType.name == training.type
        ).one()
    except NoResultFound as error:
        detail = f"Could not save training. Type {training.type} not found."
        logging.warning(detail)
        raise HTTPException(
            detail=detail, status_code=status.HTTP_404_NOT_FOUND
        ) from error
    try:
        training_difficulty = session.query(Difficulty).filter(
            Difficulty.name == training.difficulty
        ).one()
    except NoResultFound as error:
        detail = "Could not save training. Difficulty "\
            f"{training.difficulty} not found."
        logging.warning(detail)
        raise HTTPException(
            detail=detail, status_code=status.HTTP_404_NOT_FOUND
        ) from error
    foreign_keys = {
        "exercises": exercises,
        "type": training_type,
        "difficulty": training_difficulty,
    }
    fields = training.dict() | foreign_keys
    logging.debug("Exercise built %s", fields)
    return Training(**fields)
