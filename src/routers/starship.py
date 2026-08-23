"""Module defining API endpoints for starships."""

from fastapi import APIRouter, Depends, Query
from typing import Annotated
from dependencies.auth import validate_api_key
from dependencies.correlation import validate_correlation_id, CORRELATION_HEADER
from models.starship import Starship

router = APIRouter(prefix="/api/v1")

HTTP_RESPONSE_HEADERS = {
    "headers": {
        CORRELATION_HEADER: {
            "description": "A correlation/tracking ID to be sent with the next request from this client",
            "schema": {"type": "string"},
        }
    }
}


@router.get(
    "/starship-readiness",
    summary="Get a list of starships based on search parameters",
    tags=["starships"],
    dependencies=[Depends(validate_api_key), Depends(validate_correlation_id)],
    responses={
        200: HTTP_RESPONSE_HEADERS,
        204: HTTP_RESPONSE_HEADERS,
        401: HTTP_RESPONSE_HEADERS,
        422: HTTP_RESPONSE_HEADERS,
    },
)
async def get_starship_readiness(
    num_passengers: Annotated[int, Query(alias="num-passengers", ge=0)],
    hyperdrive_required: Annotated[bool, Query(alias="hyperdrive-required")],
    cargo_weight: Annotated[int, Query(alias="cargo-weight", ge=0)] = 0,
) -> list[Starship]:
    """
    Return a list of starships that can accommodate the specified search parameters.
    The list of starships will be sorted by starship name in ascending order.

    - **num-passengers**: the number of passengers to transport, not including crew
    - **hyperdrive-required**: if true, only include starships with a hyperdrive rating of 2 or higher
    - **cargo-weight**: the weight in kilograms of any additonal cargo to transport

    HTTP response status codes:

    - **200 OK**: one or more starships found
    - **204 No Content**: no starships found
    - **401 Unauthorized**: API key is not valid
    - **422 Unprocessable Content**: invalid search parameter specified
    - **500 Internal Server Error**: an unexpected error occurred
    """

    return []
