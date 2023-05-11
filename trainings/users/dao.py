"""DAO for users."""
from sqlalchemy.orm import Session

from trainings.database.models import Users


def read(session: Session, user_id: int) -> Users:
    """Read a user from the database."""
    return session.query(Users).filter(Users.id == user_id,).one()
