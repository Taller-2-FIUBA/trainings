"""Database initialization for tests."""
from typing import List, Any
from sqlalchemy.orm import Session
from trainings.database.data import (
    get_training_difficulties, get_training_types, get_exercises
)

from trainings.database.models import Training, TrainingExercise


def _insert(session, records: List[Any]) -> None:
    """Insert records."""
    for record in records:
        session.add(record)
    session.commit()


def insert_training_types(session: Session):
    """Insert training types."""
    _insert(session, get_training_types())


def insert_training_difficulties(session: Session):
    """Insert training difficulties."""
    _insert(session, get_training_difficulties())


def insert_exercises(session: Session):
    """Insert training exercises."""
    _insert(session, get_exercises())


def insert_trainings(session: Session) -> None:
    """Create initial trainings."""
    trainings = [
        Training(
            id=1,
            trainer_id="Ju6JXm1S8rVQfyC18mqL418JdgE2",
            tittle="The first training.",
            description="This is the first training.",
            type_id=1,
            difficulty_id=1,
            media="a_firebase_id",
            blocked=False,
        ),
        Training(
            id=2,
            trainer_id="tomato",
            tittle="The tomato training.",
            description="This is the tomato training.",
            type_id=2,
            difficulty_id=2,
            media="a_firebase_id",
            blocked=False,
        ),
        Training(
            id=3,
            trainer_id="naughty_trainer",
            tittle="The training to be blocked.",
            description="This is going to be blocked and unblocked.",
            type_id=3,
            difficulty_id=3,
            media="a_firebase_id",
            blocked=False,
        ),
    ]
    _insert(session, trainings)


def insert_training_exercises(session: Session) -> None:
    """Create initial training exercises."""
    exercises = [
        TrainingExercise(training_id=1, exercise_id=1, count=30, series=1),
        TrainingExercise(training_id=1, exercise_id=3, count=30, series=1),
        TrainingExercise(training_id=1, exercise_id=5, count=15, series=3),
        TrainingExercise(training_id=2, exercise_id=20, count=15, series=3),
        TrainingExercise(training_id=3, exercise_id=31, count=15, series=3),
    ]
    _insert(session, exercises)


def init_test_db(session: Session) -> None:
    """Create testing data."""
    with session as open_session:
        insert_training_types(open_session)
        insert_training_difficulties(open_session)
        insert_exercises(open_session)
        insert_trainings(open_session)
        insert_training_exercises(open_session)
