"""Requests handlers."""
import logging

from fastapi import FastAPI
from environ import to_config
from prometheus_client import start_http_server, Counter
from trainings.config import AppConfig


REQUEST_COUNTER = Counter(
    "my_failures", "Description of counter", ["endpoint", "http_verb"]
)
CONFIGURATION = to_config(AppConfig)
start_http_server(CONFIGURATION.prometheus_port)
app = FastAPI(debug=CONFIGURATION.log_level.upper() == "DEBUG")
logging.basicConfig(encoding='utf-8', level=CONFIGURATION.log_level.upper())


@app.get("/")
async def root():
    """Greet."""
    logging.info('Received request to /')
    REQUEST_COUNTER.labels("/", "get").inc()
    return {"message": "Hello World"}
