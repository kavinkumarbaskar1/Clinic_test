"""Central API route registration."""

from fastapi import APIRouter
from pydantic import BaseModel


class HealthResponse(BaseModel):
    """Health check response payload."""

    status: str


api_router = APIRouter(prefix="/api")


@api_router.get(
    "/health",
    response_model=HealthResponse,
    summary="Check service health",
    tags=["System"],
)
async def health_check() -> HealthResponse:
    """Confirm that the API process is running."""
    return HealthResponse(status="ok")
