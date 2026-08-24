"""Module containing the core business logic for mission planning."""

from mpapi.models.starship import Starship
from mpapi.services.swapi import fetch_all_starships


async def find_available_starships(
    num_passengers: int, hyperdrive_required: bool, cargo_weight: int = 0
) -> list[Starship]:
    """Retrieve a list of starships that meet the specified search criteria.

    Args:
        num-passengers: the number of passengers to transport, not including crew
        hyperdrive-required: if true, only include starships with a hyperdrive rating of 2 or higher
        cargo-weight: the weight in kilograms of any additonal cargo to transport

    Returns:
        A list of Starship objects sorted by starship name in ascending order.  If none are found
        that meet all the search criteria, an empty list is returned.
    """

    all_starships = await fetch_all_starships()

    matching_starships = []
    min_hyperdrive_rating = 2.0 if hyperdrive_required else 0.0
    for starship in all_starships:
        if (
            starship.max_passengers >= num_passengers
            and starship.hyperdrive_rating >= min_hyperdrive_rating
            and starship.cargo_capacity >= cargo_weight
        ):
            matching_starships.append(starship)

    # No need to sort matches since orignal list was already sorted
    return matching_starships
