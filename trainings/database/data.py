"""Database initialization."""
import logging
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert

from trainings.database.models import (
    Difficulty, Exercise, TrainingType
)


def get_columns_and_cells(models: List) -> List[Dict[str, Any]]:
    """Return columns and values from models, used for raw INSERT VALUES."""
    columns_and_cells = []
    for model in models:
        column_and_cell = model.__dict__
        column_and_cell.pop("_sa_instance_state")
        columns_and_cells.append(column_and_cell)
    return columns_and_cells


def get_training_types() -> List[TrainingType]:
    """Return training types records."""
    return [
        TrainingType(id=1, name="Cardio"),
        TrainingType(id=2, name="Leg"),
        TrainingType(id=3, name="Arm"),
        TrainingType(id=4, name="Chest"),
        TrainingType(id=5, name="Back"),
        TrainingType(id=6, name="Abdomen"),
    ]


def insert_in_postgres_ignoring_existing(
    session: Session, table, rows: List
) -> None:
    """
    Run an insert statement with ON CONFLICT DO NOTHING.

    This only works with PostgreSQL.
    """
    session.execute(
        insert(table)
        .values(get_columns_and_cells(rows))
        .on_conflict_do_nothing()
    )


def insert_training_types(session: Session):
    """Insert training types."""
    insert_in_postgres_ignoring_existing(
        session, TrainingType, get_training_types()
    )


def get_training_difficulties() -> List[Difficulty]:
    """Return training difficulty records."""
    return [
        Difficulty(id=1, name="Easy"),
        Difficulty(id=2, name="Medium"),
        Difficulty(id=3, name="Hard"),
    ]


def insert_training_difficulties(session: Session):
    """Insert training difficulties."""
    insert_in_postgres_ignoring_existing(
        session, Difficulty, get_training_difficulties()
    )


def get_exercises() -> List[Exercise]:
    """Return training exercise records."""
    return [
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


def insert_exercises(session: Session):
    """Insert training exercises."""
    insert_in_postgres_ignoring_existing(session, Exercise, get_exercises())


def init_db(session: Session) -> None:
    """Create basic data."""
    logging.info("Inserting initial data...")
    with session as open_session:
        logging.info("Inserting training types...")
        insert_training_types(open_session)
        logging.info("Inserting training difficulties...")
        insert_training_difficulties(open_session)
        logging.info("Inserting training exercises...")
        insert_exercises(open_session)
