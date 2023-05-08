# pylint: disable=no-name-in-module
"""Defines models for data exchange in API and between modules."""
from typing import List
from pydantic import BaseModel


class TrainingTypesOut(BaseModel):
    """Training types DTO."""

    items: List[str]
