"""Training filters."""
import logging
from typing import Any, Dict, List

from fastapi import HTTPException
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import Session

from trainings.database.models import Difficulty, Training, TrainingType
from trainings.trainings.dto import TrainingFilters, TrainingPatch


def get_criteria(session: Session, filters: TrainingFilters) -> List:
    """Get filtering criteria to search trainings."""
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


def get_columns_and_values(patch_values: TrainingPatch) -> Dict[str, Any]:
    """Translate body of patch method into update query columns and values."""
    columns_and_values = {
        k: v for k, v in patch_values.dict().items() if v is not None
    }
    return columns_and_values
