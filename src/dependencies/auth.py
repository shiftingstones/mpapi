"""Module defining the authorization dependency."""

from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security import APIKeyHeader
import os
import pwdlib

API_KEY_HEADER = APIKeyHeader(name="x-api-key")


def validate_api_key(api_key: str = Depends(API_KEY_HEADER)) -> None:
    """Check if the specified API key matches the one installed on the server."""

    # The API key on the server is hashed in an environment variable.
    installed_key_hash = os.getenv("MPAPI_KEY_HASH")
    if installed_key_hash is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No API key configured on server",
        )

    # Check if the specified API key matches the stored hash.
    pw_hash = pwdlib.PasswordHash.recommended()
    if not pw_hash.verify(api_key, installed_key_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )
