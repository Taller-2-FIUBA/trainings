"""Database initialization."""
from typing import Any, List
from sqlalchemy.orm import Session

from trainings.database.models import (
    Difficulty, Exercise, Training, TrainingExercise, TrainingType
)


def _insert(session, records: List[Any]) -> None:
    """Insert records."""
    for record in records:
        session.add(record)
    session.commit()


def insert_training_types(session: Session):
    """Insert training types."""
    training_types = [
        TrainingType(id=1, name="Cardio"),
        TrainingType(id=2, name="Leg"),
        TrainingType(id=3, name="Arm"),
        TrainingType(id=4, name="Chest"),
        TrainingType(id=5, name="Back"),
        TrainingType(id=6, name="Abdomen"),
    ]
    _insert(session, training_types)


def insert_training_difficulties(session: Session):
    """Insert training difficulties."""
    difficulties = [
        Difficulty(id=1, name="Easy"),
        Difficulty(id=2, name="Medium"),
        Difficulty(id=3, name="Hard"),
    ]
    _insert(session, difficulties)


def insert_exercises(session: Session):
    """Insert training exercises."""
    exercises = [
        Exercise(id=1, name="Walk", type_id=1, unit="metre"),
        Exercise(id=2, name="Walk", type_id=1, unit="second"),
        Exercise(id=3, name="Run", type_id=1, unit="metre"),
        Exercise(id=4, name="Run", type_id=1, unit="second"),
        Exercise(id=5, name="Jumping jacks", type_id=1, unit=None),
        Exercise(id=20, name="Squat", type_id=2, unit=None),
        Exercise(id=21, name="Lunge", type_id=2, unit=None),
        Exercise(id=22, name="Deadlift", type_id=2, unit=None),
        Exercise(id=30, name="Bicep curl", type_id=3, unit=None),
        Exercise(id=31, name="Hammer curl", type_id=3, unit=None),
        Exercise(id=40, name="Tricep dips", type_id=3, unit=None),
        Exercise(id=41, name="Close grip push up", type_id=3, unit=None),
        Exercise(id=42, name="Push-down", type_id=3, unit=None),
        Exercise(id=50, name="Lateral raise", type_id=3, unit=None),
        Exercise(id=51, name="Front raise", type_id=3, unit=None),
        Exercise(id=52, name="Arnold press", type_id=3, unit=None),
        Exercise(id=60, name="Push up", type_id=4, unit=None),
        Exercise(id=61, name="Bench press", type_id=4, unit=None),
        Exercise(id=62, name="Fly", type_id=4, unit=None),
        Exercise(id=70, name="Pull-down", type_id=5, unit=None),
        Exercise(id=71, name="Pull-up", type_id=5, unit=None),
        Exercise(id=72, name="Bent-over row", type_id=5, unit=None),
        Exercise(id=80, name="Crunch", type_id=6, unit=None),
        Exercise(id=81, name="Bicycle crunch", type_id=6, unit=None),
        Exercise(id=82, name="Plank", type_id=6, unit=None),
    ]
    _insert(session, exercises)


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
        ),
        Training(
            id=2,
            trainer_id="tomato",
            tittle="The tomato training.",
            description="This is the tomato training.",
            type_id=2,
            difficulty_id=2,
            media="a_firebase_id",
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
    ]
    _insert(session, exercises)


def init_db(session: Session) -> None:
    """Create basic data."""
    with session as open_session:
        insert_training_types(open_session)
        insert_training_difficulties(open_session)
        insert_exercises(open_session)
        insert_trainings(open_session)
        insert_training_exercises(open_session)
