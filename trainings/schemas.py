# pylint: disable=no-name-in-module
"""Defines models for data exchange in API and between modules."""
from typing import List, Optional
from pydantic import BaseModel


class Exercise(BaseModel):
    """Exercise DTO."""

    name: str
    type: str
    unit: Optional[str]
    count: int
    series: Optional[int]


class TrainingIn(BaseModel):
    """Training DTO."""

    tittle: str
    description: str
    type: str
    difficulty: str
    media: Optional[str]
    exercises: List[Exercise]


class TrainingOut(TrainingIn):
    """Training DTO."""

    id: int
    rating: int


class TrainingsWithPagination(BaseModel):
    """To return data."""

    items: List[TrainingOut]
    offset: Optional[int]
    limit: Optional[int]
