"""A module that defines the logging configuration used throughout the app."""

import os
import logging
from logging.handlers import RotatingFileHandler
from fastapi import Request
from asgi_correlation_id.log_filters import CorrelationIdFilter
from pythonjsonlogger.json import JsonFormatter
from http import HTTPStatus

# Save the log file to /var/log in docker, otherwise to the working directory for local testing
MPAPI_LOG_FILE = (
    "/var/log/mpapi.log" if os.access("/var/log/", os.W_OK) else "mpapi.log"
)

# Configure the root logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Log the first 8 characters of the correlation ID with every request
correlation_log_filter = CorrelationIdFilter(uuid_length=8, default_value="-")
logger.addFilter(correlation_log_filter)

# The handler and formatter to show output in the console window
console_log_handler = logging.StreamHandler()
console_log_formatter = logging.Formatter(
    fmt="%(levelname)s:\t\b%(asctime)s %(name)s [%(correlation_id)s] %(message)s"
)
console_log_handler.setFormatter(console_log_formatter)
logger.addHandler(console_log_handler)

# The handle and formatter to log messages to a JSON file
file_log_handler = RotatingFileHandler(
    MPAPI_LOG_FILE, maxBytes=10 * 1024 * 1024, backupCount=5, encoding="utf-8"
)
file_log_formatter = JsonFormatter(
    fmt=["asctime", "correlation_id", "levelname", "name", "message"],
    rename_fields={"asctime": "timestamp", "levelname": "level", "name": "logger"},
)
file_log_handler.setFormatter(file_log_formatter)
logger.addHandler(file_log_handler)


async def log_requests_middleware(request: Request, call_next):
    """Middleware used to log every access request."""

    response = await call_next(request)

    # Combine the response code with its corresponding "user friendly" description
    http_status = HTTPStatus(response.status_code)
    response_status = f"{http_status.value} {http_status.phrase}"

    # Client host and port number
    client_host = request.client.host if request.client else ""
    client_port = request.client.port if request.client else ""
    client = f"{client_host}:{client_port}"

    logger.info(f"{client} '{request.method} {request.url}' {response_status}")

    return response
