"""DAO for trainings."""
from sqlalchemy.orm import Session
from trainings.database.models import (
    Training,
)


def browse(session: Session, offset: int, limit: int):
    """Return all trainings."""
    return session.query(Training).offset(offset).limit(limit).all()
