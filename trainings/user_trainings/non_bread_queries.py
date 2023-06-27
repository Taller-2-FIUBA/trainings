"""Helper queries for users's favourite trainings."""
import logging
from sqlalchemy.orm import Session
from trainings.database.models import UserTraining


def get_count(session: Session, user_id: str) -> int:
    """Return how many favourite trainings a user has."""
    logging.info("Running count query...")
    return session.query(UserTraining).filter(
        UserTraining.user_id == user_id
    ).count()
