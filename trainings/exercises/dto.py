# pylint: disable=no-name-in-module
"""Defines models for data exchange in API and between modules."""
from typing import List, Optional
from pydantic import BaseModel


class Exercise(BaseModel):
    """Training DTO."""

    name: str
    type: str
    unit: Optional[str]


class ExercisesOut(BaseModel):
    """Training exercises DTO."""

    items: List[Exercise]
