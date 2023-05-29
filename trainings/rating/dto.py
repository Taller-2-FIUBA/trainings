# pylint: disable=no-name-in-module
"""Defines models for data exchange in API."""
from pydantic import BaseModel


class TrainingRating(BaseModel):
    """Rating DTO."""

    rate: float
