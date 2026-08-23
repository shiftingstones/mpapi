"""Module containing the main entry point for the FastAPI app."""

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from routers.starship import router as starship_router

# Endpoints are defined in separate modules under the routers package.
app = FastAPI()
app.include_router(starship_router)


@app.get("/", include_in_schema=False)
async def redirect_root() -> RedirectResponse:
    """Redirect the index/root path to the Swagger docs."""
    return RedirectResponse(url="/docs")
