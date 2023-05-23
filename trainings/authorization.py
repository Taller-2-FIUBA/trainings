"""Authorize users to perform actions."""
import logging
from typing import Dict

from fastapi import HTTPException, Header, status
from httpx import Client

from trainings.config import AppConfig


def get_permissions(
    headers: Header,
    http_client: Client,
    config: AppConfig
) -> Dict[str, str]:
    """Get user details from token in request header."""
    url = f"http://{config.auth.host}/auth/credentials"
    auth_header = headers.get("Authorization")
    if not auth_header:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Authorization header MUST BE send."
        )
    credentials = http_client.get(url, headers={"Authorization": auth_header})
    if credentials.status_code != status.HTTP_200_OK:
        logging.error(
            "Error getting token. Status code: %d, Error: %s",
            credentials.status_code,
            credentials.json()
        )
        raise HTTPException(
            status_code=credentials.status_code,
            detail=credentials.json()
        )
    try:
        return credentials.json()["data"]
    except Exception as json_exception:
        msg = "Error getting credentials (Maybe token is invalid?)"
        logging.error("%s. Credentials %s", msg, credentials)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=msg
        ) from json_exception


def assert_can_create_training(permissions: Dict[str, str]) -> bool:
    """Raise HTTPException if user can't create training."""
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
