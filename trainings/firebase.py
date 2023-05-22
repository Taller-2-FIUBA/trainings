"""Connect to firebase."""
import logging
import random
import string
from typing import Any, Dict, Optional
from firebase_admin import initialize_app, storage, get_app
from firebase_admin.credentials import Certificate
from google.cloud.exceptions import NotFound

from trainings.config import AppConfig


def get_file_name(trainer_id: str) -> str:
    """Return a file name for the training media."""
    return trainer_id + "-" + ''.join(
        random.choices(string.ascii_uppercase + string.digits, k=32)
    )


def get_certificate(config: AppConfig) -> Dict[str, Any]:
    """Create certificate data for firebase API."""
    return {
        "type": config.firebase.type,
        "project_id": config.firebase.project_id,
        "private_key_id": config.firebase.private_key_id,
        "private_key": config.firebase.private_key,
        "client_email": config.firebase.client_email,
        "client_id": config.firebase.client_id,
        "auth_uri": config.firebase.auth_uri,
        "token_uri": config.firebase.token_uri,
        "auth_provider_x509_cert_url":
        config.firebase.auth_provider_x509_cert_url,
        "client_x509_cert_url": config.firebase.client_x509_cert_url,
    }


def initialize(config: AppConfig):
    """Configure firebase."""
    logging.debug("Cheking if firebase is initialized...")
    try:
        app = get_app()
    except ValueError as e:
        logging.info("Firebase is not initialized %s", e)
        app = None
    if not app:
        logging.info("Initializing firebase...")
        initialize_app(
            Certificate(get_certificate(config)),
            {"storageBucket": config.firebase.storage_bucket}
        )
    else:
        logging.debug("Firebase initialized no need to initialize again.")


def save(media: str, trainer_id: str, config: AppConfig) -> str:
    """Save media in firebase and return id."""
    initialize(config)
    logging.debug("Saving firebase media: %s", media)
    bucket = storage.bucket()
    file_name = get_file_name(trainer_id)
    blob = bucket.blob(file_name)
    logging.info("Uploading media in %s...", file_name)
    blob.upload_from_string(media)
    logging.info("Saved media in %s.", file_name)
    return file_name


def read(name: str, config: AppConfig) -> Optional[str]:
    """Read file from firebase."""
    initialize(config)
    bucket = storage.bucket()
    blob = bucket.blob(name)
    logging.info("Downloading media %s...", name)
    try:
        media = blob.download_as_text()
    except NotFound as e:
        logging.error("Blob of media named %s not found. Error: %s", name, e)
        media = None
    return media
