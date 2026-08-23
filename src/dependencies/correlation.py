"""Module defining the correlation ID dependency."""

from fastapi import Header
from typing import Annotated

CORRELATION_HEADER = "x-correlation-id"


async def validate_correlation_id(
    correlation_id: Annotated[str | None, Header(alias=CORRELATION_HEADER)] = None,
):
    """Currently this dependency function is only used to ensure that the API
    (optionally) accepts a correlation ID in the request header.  If we want to
    take action in the future based on the ID, this would be the place to add it.
    """
    pass
