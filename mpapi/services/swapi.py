"""A module containing functions to fetch data from the Star Wars API (swapi.info).

The module currently contains a single public function to fetch all starships.  More
functions could be added in the future to fetch other types of data from SWAPI (e.g.,
films, people, planets).

Typical usage example:
    from services.swapi import fetch_all_starships
    starships = await fetch_all_starships()
"""

import anyio, anyio.to_thread
import requests

from mpapi.models.starship import Starship
from mpapi.core.utils import parse_int, parse_float

SWAPI_STARSHIPS_URL = "https://swapi.info/api/starships"


def _fetch_starships() -> list[dict]:
    """Helper function to fetch starships.

    Retrieves the JSON dump of all starships from SWAPI and then returns them as a
    list of dictionaries.  No data conversion is performed in this function; the data
    is returned as-is from SWAPI.  All values in the returned dictionaries are strings,
    even if they represent numeric values.

    Returns:
        A list of dictionaries with string values, each representing a starship.
    """
    response = requests.get(
        SWAPI_STARSHIPS_URL,
        headers={"Accept": "application/json"},
        timeout=5,
    )
    response.raise_for_status()

    payload = response.json()
    if not isinstance(payload, list):
        raise ValueError("SWAPI returned an unexpected response")

    return payload


async def fetch_all_starships() -> list[Starship]:
    """Fetch all starships from SWAPI and return them as a list of Starship objects.

    This function asynchronously fetches the raw starship data from SWAPI, converts the
    string values to the appropriate numeric types if necessary, and then returns a list
    of Starship objects.  The list is sorted by starship name in ascending order.

    Returns:
        A list of Starship objects, sorted by starship name in ascending order (case-insensitive).
    """
    raw_data = await anyio.to_thread.run_sync(_fetch_starships)
    list_of_starships = []

    for entry in raw_data:
        attr = {}
        attr["name"] = entry["name"].strip()
        attr["model"] = entry["model"].strip()
        attr["class"] = entry["starship_class"].strip()

        attr["cargo_capacity"] = parse_int(entry["cargo_capacity"])
        attr["max_crew"] = parse_int(entry["crew"])
        attr["max_passengers"] = parse_int(entry["passengers"])
        attr["hyperdrive_rating"] = parse_float(entry["hyperdrive_rating"])

        list_of_starships.append(Starship(**attr))

    list_of_starships.sort(key=lambda starship: starship.name.lower())
    return list_of_starships


if __name__ == "__main__":
    """When this module is executed as a script using 'python -m services.swapi',
    run a standalone test that fetches all the starships from SWAPI and then dumps
    the Starship objects to the console.
    """
    starships = anyio.run(fetch_all_starships)
    for starship in starships:
        print(starship.model_dump())
