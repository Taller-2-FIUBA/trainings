"""DAO for trainings owned by a user."""
from sqlalchemy.orm import Session

from trainings.database.models import UserTraining


def add(session: Session, user_id: str, training_id: int) -> None:
    """Read a user from the database."""
    session.add(UserTraining(user_id=user_id, training_id=training_id))
    session.commit()
