"""DAO for training ratings by a user."""
from sqlalchemy.orm import Session

from trainings.database.models import UserRatesTraining


def add(
    session: Session, user_id: str, training_id: int, ratting: float
) -> None:
    """Rate a training."""
    session.add(
        UserRatesTraining(
            user_id=user_id, training_id=training_id, ratting=ratting
        )
    )
    session.commit()
