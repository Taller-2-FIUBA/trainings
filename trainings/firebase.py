"""Connect to firebase."""
import logging
import random
import string
from firebase_admin import initialize_app, storage
from firebase_admin.credentials import Certificate

from trainings.config import AppConfig


def get_file_name(trainer_id: str) -> str:
    """Return a file name for the training media."""
    return trainer_id + ''.join(
        random.choices(string.ascii_uppercase + string.digits, k=32)
    )


def save(media: str, trainer_id: str, config: AppConfig) -> str:
    """Save media in firebase and return id."""
    logging.debug("Saving in firebase: %s", media)
    logging.info("Initializing firebase...")
    initialize_app(
        Certificate(config.firebase.__dict__),
        {"storageBucket": config.firebase.storagebucket}
    )
    bucket = storage.bucket()
    file_name = get_file_name(trainer_id)
    blob = bucket.blob(file_name)
    logging.info("Uploading media in %s...", file_name)
    blob.upload_from_string(media)
    logging.info("Saved media in %s.", file_name)
    return file_name
