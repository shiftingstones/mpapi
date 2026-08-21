from fastapi import FastAPI, APIRouter, Query
from typing import Annotated
from models.starship import Starship

app = FastAPI()
router = APIRouter(prefix="/api/v1")


@router.get(
    "/starship-readiness",
    summary="Get a list of starships based on search parameters",
    tags=["starships"],
)
async def get_starship_readiness(
    num_passengers: Annotated[int, Query(ge=0)],
    hyperdrive_required: Annotated[bool, Query()],
    cargo_weight: Annotated[int, Query(ge=0)] = 0,
) -> list[Starship]:
    """
    Return a list of starships that can accommodate the specified search parameters.
    The list of starships will be sorted by starship name in ascending order.

    - **num_passengers**: the number of passengers to transport, not including crew
    - **hyperdrive_required**: if true, only include starships with a hyperdrive rating of 2 or higher
    - **cargo_weight**: the weight of any additonal cargo to transport

    HTTP response status codes:

    - **200 OK**: one or more starships found
    - **204 No Content**: no starships found
    - **401 Unauthorized**: API key is not valid
    - **422 Unprocessable Content**: invalid search parameter specified
    - **500 Internal Server Error**: an unexpected error occurred
    """

    return []


app.include_router(router)
