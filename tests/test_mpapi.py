"""Module containing test cases for the Star Wars mission planning API."""

import pytest
import os
from fastapi.testclient import TestClient
from fastapi import status
from httpx2 import Response
from mpapi.app import app
from mpapi.models.starship import Starship

API_ENDPOINT = "/api/v1/starship-readiness"

client = TestClient(app)


@pytest.fixture
def configure_api_key():
    # If we're not running in docker, set up an environment variable with our API key
    if not os.getenv("MPAPI_KEY_HASH"):
        os.environ["MPAPI_KEY_HASH"] = (
            "$argon2id$v=19$m=65536,t=3,p=4$/WXPTY3c/F3KFvJxFew73Q$OVr6Q0qiNzZm1s0tMvhsqXZ0P30Qx7nbVO2h9hzf7ko"
        )


def test_missing_api_key():
    response: Response = client.get(API_ENDPOINT)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Not authenticated"}


def test_invalid_api_key(configure_api_key):
    response: Response = client.get(
        API_ENDPOINT, headers={"x-api-key": "invalidapikey"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Invalid API key"}


def test_get_starship_readiness_no_results(configure_api_key):
    response: Response = client.get(
        "/api/v1/starship-readiness?num-passengers=5000000&hyperdrive-required=true",
        headers={"x-api-key": "hansolofalcon"},
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response.content == b""


def test_get_starship_readiness(configure_api_key):
    response: Response = client.get(
        "/api/v1/starship-readiness?num-passengers=100&hyperdrive-required=true",
        headers={"x-api-key": "hansolofalcon"},
    )

    assert response.status_code == 200

    attr = {
        "name": "Executor",
        "model": "Executor-class star dreadnought",
        "class": "Star dreadnought",
        "cargo_capacity": 250000000,
        "max_crew": 279144,
        "max_passengers": 38000,
        "hyperdrive_rating": 2,
    }
    expected_starship = Starship(**attr)

    response_json = response.json()
    assert len(response_json) == 4
    assert response_json[3] == expected_starship.model_dump()
