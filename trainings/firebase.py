"""Connect to firebase."""
import logging
import random
import string
from typing import Any, Dict
from firebase_admin import initialize_app, storage, get_app
from firebase_admin.credentials import Certificate

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


def save(media: str, trainer_id: str, config: AppConfig) -> str:
    """Save media in firebase and return id."""
    logging.debug("Saving firebase media: %s", media)
    logging.debug("Cheking if firebase is initialized...")
    if not get_app():
        logging.info("Initializing firebase...")
        initialize_app(
            Certificate(get_certificate(config)),
            {"storageBucket": config.firebase.storage_bucket}
        )
    bucket = storage.bucket()
    file_name = get_file_name(trainer_id)
    blob = bucket.blob(file_name)
    logging.info("Uploading media in %s...", file_name)
    blob.upload_from_string(media)
    logging.info("Saved media in %s.", file_name)
    return file_name
