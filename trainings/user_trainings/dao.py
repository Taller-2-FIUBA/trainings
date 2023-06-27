"""DAO for trainings owned by a user."""
from sqlalchemy.orm import Session

from trainings.database.models import (
    UserTraining,
    Users,
)


def browse(
    session: Session, user_id: str, offset: int, limit: int
) -> Users:
    """Get all trainings of a user."""
    return session.query(Users)\
        .filter(Users.id == user_id)\
        .offset(offset).limit(limit).one()


def add(session: Session, user_id: str, training_id: int) -> None:
    """Add favourite training for a user."""
    session.add(UserTraining(user_id=user_id, training_id=training_id))
    session.commit()


def delete(session: Session, user_id: str, training_id: int) -> None:
    """Delete favourite training for a user."""
    session.query(UserTraining).where(
        UserTraining.user_id == user_id,
        UserTraining.training_id == training_id,
    ).delete()
    session.commit()
