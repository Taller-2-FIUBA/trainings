# pylint: disable=no-name-in-module
"""Health check endpoint."""
from pydantic import BaseModel


class HealthCheckDto(BaseModel):
    uptime: float
