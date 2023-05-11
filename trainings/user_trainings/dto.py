# pylint: disable=no-name-in-module
"""Defines models for data exchange in API."""
from pydantic import BaseModel


class UserTrainingIn(BaseModel):
    """Exercise DTO."""

    training_id: int
