"""Authorize users to perform actions."""
import logging
from typing import Dict
from fastapi import HTTPException, status


def assert_can_create_training(permissions: Dict[str, str]) -> bool:
    """Raise HTTPException if user can't create training"""
    # When role accept trainer for value change this.
    logging.info("Validating that user can create trainings...")
    if permissions["role"] != "user":
        logging.error(
            "User with role %s can't create training", permissions["role"]
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to create trainings."
        )
    return True
