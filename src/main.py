"""Module containing the main entry point for the FastAPI app."""

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from asgi_correlation_id import CorrelationIdMiddleware
from routers.starship import router as starship_router
from dependencies.correlation import CORRELATION_HEADER

# Endpoints are defined in separate modules under the routers package.
app = FastAPI()
app.include_router(starship_router)

# Add middleware to accept (or generate) a correlation ID with every request.
app.add_middleware(CorrelationIdMiddleware, header_name=CORRELATION_HEADER)


@app.get("/", include_in_schema=False)
async def redirect_root() -> RedirectResponse:
    """Redirect the index/root path to the Swagger docs."""
    return RedirectResponse(url="/docs")
