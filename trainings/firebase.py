"""Connect to firebase."""
import logging


# Dummy temporary implementation.
def save(media: str) -> str:
    """Save media in firebase and return id."""
    logging.debug("Saving %s in firebase...", media)
    return "a_firebase_id"
