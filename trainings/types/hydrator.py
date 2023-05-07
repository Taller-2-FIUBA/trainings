"""Hydrate DTOs from database objects."""
from typing import List
from trainings.database.models import TrainingType
from trainings.types.dto import TrainingTypesOut


def hydrate(training_types: List[TrainingType]) -> TrainingTypesOut:
    """Create an HTTP DTO from a database model object."""
    training_types_out = TrainingTypesOut(items=[])
    for training_type in training_types:
        training_types_out.items.append(training_type.name)
    return training_types_out
