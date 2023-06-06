"""Database initialization for tests."""
from typing import List, Any
from sqlalchemy.orm import Session
from trainings.database.data import (
    get_training_difficulties, get_training_types, get_exercises
)

from trainings.database.models import (
    Training,
    TrainingExercise,
    UserRatesTraining,
    UserTraining,
    Users
)


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
            title="The first training.",
            description="This is the first training.",
            type_id=1,
            difficulty_id=1,
            media=None,
            blocked=False,
        ),
        Training(
            id=2,
            trainer_id="tomato",
            title="The tomato training.",
            description="This is the tomato training.",
            type_id=2,
            difficulty_id=2,
            media=None,
            blocked=False,
        ),
        Training(
            id=3,
            trainer_id="naughty_trainer",
            title="The training to be blocked.",
            description="This is going to be blocked and unblocked.",
            type_id=3,
            difficulty_id=3,
            media=None,
            blocked=False,
        ),
        Training(
            id=4,
            trainer_id="indecisive_trainer",
            title="This training will be modified, trainer is indecisive.",
            description="This is going to change.",
            type_id=3,
            difficulty_id=3,
            media=None,
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
        TrainingExercise(training_id=4, exercise_id=31, count=15, series=3),
    ]
    _insert(session, exercises)


def insert_users(session: Session):
    """Insert toy users."""
    _insert(
        session,
        [
            Users(
                id="1",
                email="blah",
                username="blah",
                name="blah",
                surname="blah",
                height=1.0,
                weight=1,
                birth_date="blah",
                location="blah",
                registration_date="blah",
                is_athlete=False,
                is_blocked=False,
            ),
            Users(
                id="2",
                email="IHaveFavouriteTrainings",
                username="IHaveFavouriteTrainings",
                name="IHaveFavouriteTrainings",
                surname="IHaveFavouriteTrainings",
                height=1.0,
                weight=1,
                birth_date="IHaveFavouriteTrainings",
                location="IHaveFavouriteTrainings",
                registration_date="IHaveFavouriteTrainings",
                is_athlete=False,
                is_blocked=False,
            ),
            Users(
                id="3",
                email="IDoNotHaveFavouriteTrainings",
                username="IDoNotHaveFavouriteTrainings",
                name="IDoNotHaveFavouriteTrainings",
                surname="IDoNotHaveFavouriteTrainings",
                height=1.0,
                weight=1,
                birth_date="IDoNotHaveFavouriteTrainings",
                location="IDoNotHaveFavouriteTrainings",
                registration_date="IDoNotHaveFavouriteTrainings",
                is_athlete=False,
                is_blocked=False,
            ),
            Users(
                id="4",
                email="UserThatDeleteFavouriteTrainings",
                username="UserThatDeleteFavouriteTrainings",
                name="UserThatDeleteFavouriteTrainings",
                surname="UserThatDeleteFavouriteTrainings",
                height=1.0,
                weight=1,
                birth_date="UserThatDeleteFavouriteTrainings",
                location="UserThatDeleteFavouriteTrainings",
                registration_date="UserThatDeleteFavouriteTrainings",
                is_athlete=True,
                is_blocked=False,
            ),
        ]
    )


def insert_user_trainings(session: Session):
    """Insert user trainings."""
    _insert(
        session,
        [
            UserTraining(user_id=2, training_id=1),
            UserTraining(user_id=2, training_id=2),
            UserTraining(user_id=4, training_id=1),
        ]
    )


def insert_user_ratings(session: Session):
    """Insert ratings of a training by a user."""
    _insert(
        session,
        [
            UserRatesTraining(user_id=1, training_id=1, rating=4.5),
            UserRatesTraining(user_id=2, training_id=1, rating=3.5),
        ]
    )


def init_test_db(session: Session) -> None:
    """Create testing data."""
    with session as open_session:
        insert_training_types(open_session)
        insert_training_difficulties(open_session)
        insert_exercises(open_session)
        insert_trainings(open_session)
        insert_training_exercises(open_session)
        insert_users(open_session)
        insert_user_trainings(open_session)
        insert_user_ratings(open_session)
