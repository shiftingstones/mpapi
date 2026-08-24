"""A module that defines the logging configuration used throughout the app.

Log files are saved to /var/log in docker, otherwise to the working directory
for local testing.  We configure two JSON log files -- first the root logger for
application logs and then a second logger to track all API access requests.  Both
loggers also dump the same messages to the console window.
"""

import os
import logging
from logging.handlers import RotatingFileHandler
from fastapi import Request
from asgi_correlation_id.log_filters import CorrelationIdFilter
from pythonjsonlogger.json import JsonFormatter
from http import HTTPStatus

# Begin configuration of the application (root) logger
MPAPI_APP_LOG_FILE = (
    "/var/log/mpapi_app.log" if os.access("/var/log/", os.W_OK) else "mpapi_app.log"
)

# Configure the root logger
root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)

# Log the first 8 characters of the correlation ID with every request
root_correlation_filter = CorrelationIdFilter(uuid_length=8, default_value="-")
root_logger.addFilter(root_correlation_filter)

# The handler and formatter to show output in the console window
root_console_handler = logging.StreamHandler()
root_console_formatter = logging.Formatter(
    fmt="%(levelname)s:\t\b%(asctime)s %(name)s [%(correlation_id)s]  %(message)s"
)
root_console_handler.setFormatter(root_console_formatter)
root_logger.addHandler(root_console_handler)

# The handler and formatter to log messages to a JSON file
root_file_handler = RotatingFileHandler(
    MPAPI_APP_LOG_FILE, maxBytes=10 * 1024 * 1024, backupCount=5, encoding="utf-8"
)
root_file_formatter = JsonFormatter(
    fmt=["asctime", "correlation_id", "levelname", "name", "message"],
    rename_fields={"asctime": "timestamp", "levelname": "level", "name": "logger"},
)
root_file_handler.setFormatter(root_file_formatter)
root_logger.addHandler(root_file_handler)

# Begin configuration of the API access logger
MPAPI_ACCESS_LOG_FILE = (
    "/var/log/mpapi_access.log"
    if os.access("/var/log/", os.W_OK)
    else "mpapi_access.log"
)

# Configure the access logger.  The access logs do NOT propagate up to the root logger.
access_logger = logging.getLogger("mpapi.access")
access_logger.setLevel(logging.DEBUG)
access_logger.propagate = False

# Log the first 8 characters of the correlation ID with every request
access_correlation_filter = CorrelationIdFilter(uuid_length=8, default_value="-")
access_logger.addFilter(access_correlation_filter)

# The handler and formatter to show output in the console window
access_console_handler = logging.StreamHandler()
access_console_formatter = logging.Formatter(
    fmt="%(levelname)s:\t\b%(asctime)s [%(correlation_id)s] %(message)s"
)
access_console_handler.setFormatter(access_console_formatter)
access_logger.addHandler(access_console_handler)

# The handler and formatter to log messages to a JSON file
access_file_handler = RotatingFileHandler(
    MPAPI_ACCESS_LOG_FILE, maxBytes=10 * 1024 * 1024, backupCount=5, encoding="utf-8"
)
access_file_formatter = JsonFormatter(
    fmt=["asctime", "correlation_id", "levelname", "message"],
    rename_fields={"asctime": "timestamp", "levelname": "level"},
)
access_file_handler.setFormatter(access_file_formatter)
access_logger.addHandler(access_file_handler)


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

    access_logger.info(f"{client} '{request.method} {request.url}' {response_status}")

    return response


# Begin configuration of the urllib3 logger
urllib3_logger = logging.getLogger("urllib3.connectionpool")
urllib3_logger.setLevel(logging.DEBUG)

# Without this correlation filter, urllib3 throws exceptions on DEBUG
urllib3_correlation_filter = CorrelationIdFilter(uuid_length=8, default_value="-")
urllib3_logger.addFilter(urllib3_correlation_filter)


# urllib3 is chatty, filter out DEBUG messages from the console but keep them in the application log
def urllib3_filter(record: logging.LogRecord) -> bool:
    return True if record.levelno >= logging.INFO else False


root_console_handler.addFilter(urllib3_filter)
