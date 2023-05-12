"""Connect to firebase."""
import logging


# Dummy temporary implementation.
def save(media: str) -> str:
    """Save media in firebase and return id."""
    logging.debug("Saving in firebase: %s", media)
    media_id = "a_firebase_id"
    logging.info("Saved media of id %s.", media_id)
    return media_id
