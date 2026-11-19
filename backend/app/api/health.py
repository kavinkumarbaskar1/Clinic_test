"""Safe service health endpoint."""

from typing import Literal

from fastapi import APIRouter
from pydantic import BaseModel


class HealthResponse(BaseModel):
    """Health check response payload with no sensitive service details."""

    status: Literal["ok"]


router = APIRouter(tags=["System"])


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Check service health",
)
async def health_check() -> HealthResponse:
    """Confirm that the API process is running."""
    return HealthResponse(status="ok")
