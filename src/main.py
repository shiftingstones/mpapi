"""Module containing the main entry point for the FastAPI app."""

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware
from asgi_correlation_id import CorrelationIdMiddleware
from routers.starship import router as starship_router
from dependencies.correlation import CORRELATION_HEADER
from core.logging import log_requests_middleware

# Endpoints are defined in separate modules under the routers package
app = FastAPI()
app.include_router(starship_router)

# Add middleware to log all requests
app.add_middleware(BaseHTTPMiddleware, dispatch=log_requests_middleware)

# Add middleware to accept (or generate) a correlation ID with every request
app.add_middleware(CorrelationIdMiddleware, header_name=CORRELATION_HEADER)


@app.get("/", include_in_schema=False)
async def redirect_root() -> RedirectResponse:
    """Redirect the index/root path to the Swagger docs."""
    return RedirectResponse(url="/docs")
