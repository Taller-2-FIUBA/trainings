"""Helper methods."""
import logging

from fastapi import HTTPException, status
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import Session

from trainings.database.models import Training, Users
from trainings.trainings.dao import read as trainings_dao_read
from trainings.users.dao import read as user_dao_read
from trainings.rating.dao import read as rating_dao_read


def read_user(open_session: Session, user_id: int) -> Users:
    """Get user or throw HTTP 404 error."""
    try:
        logging.info("Searching for userId %s...", user_id)
        return user_dao_read(open_session, user_id)
    except NoResultFound as error:
        raise HTTPException(
            detail="User not found.", status_code=status.HTTP_404_NOT_FOUND
        ) from error


def read_training(open_session: Session, training_id: int) -> Training:
    """Get training or throw HTTP 404 error."""
    try:
        logging.info("Searching for trainingId %s...", training_id)
        return trainings_dao_read(open_session, training_id)
    except NoResultFound as error:
        raise HTTPException(
            detail="Training not found.", status_code=status.HTTP_404_NOT_FOUND
        ) from error


def read_rating(
    open_session: Session, user_id: int, training_id: int
) -> Training:
    """Get rating of a training by a user or throw HTTP 404 error."""
    try:
        logging.info("Searching for rating...")
        return rating_dao_read(open_session, user_id, training_id)
    except NoResultFound as error:
        raise HTTPException(
            detail="Rating not found.", status_code=status.HTTP_404_NOT_FOUND
        ) from error
