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

    trainer_id: str
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
    blocked: bool


class TrainingsWithPagination(BaseModel):
    """To return data."""

    items: List[TrainingOut]
    offset: Optional[int]
    limit: Optional[int]
    count: Optional[int]


class TrainingFilters(BaseModel):
    """Search trainings filtering by fields."""

    offset: int
    limit: int
    trainer_id: Optional[str]
    type: Optional[str]
    difficulty: Optional[str]
    title: Optional[str]


class TrainingPatch(BaseModel):
    """Fields from training that can be updated."""

    tittle: Optional[str]
    description: Optional[str]
    difficulty: Optional[str]
    media: Optional[str]
    blocked: Optional[bool]
