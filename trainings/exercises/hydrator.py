"""Hydrate DTOs from database objects."""
from typing import List
from trainings.database.models import Exercise
from trainings.exercises.dto import Exercise as ExerciseDto, ExercisesOut


def hydrate(exercises: List[Exercise]) -> ExercisesOut:
    """Create an HTTP DTO from a database model object."""
    exercises_out = ExercisesOut(items=[])
    for exercise in exercises:
        exercises_out.items.append(
            ExerciseDto(
                name=exercise.name,
                type=exercise.type.name,
                unit=exercise.unit,
            )
        )
    return exercises_out
