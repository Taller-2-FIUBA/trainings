"""Training filters."""
import logging
from typing import List

from fastapi import HTTPException
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import Session

from trainings.database.models import Difficulty, Training, TrainingType
from trainings.trainings.dto import TrainingFilters


def get_criteria(session: Session, filters: TrainingFilters) -> List:
    criteria = []
    logging.info("Building search criteria...")
    if filters.trainer_id:
        criteria.append(Training.trainer_id == filters.trainer_id)
    if filters.type:
        try:
            criteria.append(
                Training.type == session.query(TrainingType).filter(
                    TrainingType.name == filters.type,
                ).one()
            )
        except NoResultFound as error:
            detail = f"Could not save training. Type {filters.type} not found."
            logging.warning(detail)
            raise HTTPException(detail=detail, status_code=400) from error
    if filters.difficulty:
        try:
            criteria.append(
                Training.difficulty == session.query(Difficulty).filter(
                    Difficulty.name == filters.difficulty,
                ).one()
            )
        except NoResultFound as error:
            detail = "Could not save training. "\
                + f"Difficulty {filters.difficulty} not found."
            logging.warning(detail)
            raise HTTPException(detail=detail, status_code=400) from error
    logging.debug("Search criteria: %s", criteria)
    return criteria
