from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security import APIKeyHeader
import os
import pwdlib

api_key_header = APIKeyHeader(name="X-Api-Key")


def validate_api_key(api_key: str = Depends(api_key_header)) -> None:
    installed_key_hash = os.getenv("MPAPI_KEY_HASH")
    if installed_key_hash is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No API key configured on server",
        )

    pw_hash = pwdlib.PasswordHash.recommended()
    if not pw_hash.verify(api_key, installed_key_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )
