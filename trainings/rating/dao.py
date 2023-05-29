"""DAO for training ratings by a user."""
from sqlalchemy.orm import Session
from trainings.database.models import UserRatesTraining


def read(
    session: Session, user_id: int, training_id: int
) -> UserRatesTraining:
    """Rate a training."""
    return session.query(UserRatesTraining).filter(
        UserRatesTraining.user_id == user_id,
        UserRatesTraining.training_id == training_id,
    ).one()


def add(
    session: Session, user_id: int, training_id: int, rating: float
) -> None:
    """Rate a training."""
    query = session.query(UserRatesTraining).where(
        UserRatesTraining.user_id == user_id,
        UserRatesTraining.training_id == training_id,
    )
    if query.first():
        query.update(values={"rating": rating})
    else:
        session.add(
            UserRatesTraining(
                user_id=user_id, training_id=training_id, rating=rating
            )
        )
    session.commit()
