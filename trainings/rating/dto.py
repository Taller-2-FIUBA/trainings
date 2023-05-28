# pylint: disable=no-name-in-module
"""Defines models for data exchange in API."""
from pydantic import BaseModel


class TrainingRatingIn(BaseModel):
    """Rating DTO."""

    rate: float
