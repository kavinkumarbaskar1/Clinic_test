"""Role-based authorization helpers for staff routes."""

from collections.abc import Iterable

from fastapi import HTTPException, status

from app.security.context import StaffActorContext, StaffRole


def require_staff_role(
    actor: StaffActorContext | None,
    allowed_roles: Iterable[StaffRole],
) -> StaffActorContext:
    """Require a staff actor with at least one allowed role."""
    allowed = frozenset(allowed_roles)
    if actor is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Authorized staff role required.",
        )
    if actor.roles.isdisjoint(allowed):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Staff role is not authorized for this resource.",
        )
    return actor


def require_staff_schedule_access(
    actor: StaffActorContext | None,
) -> StaffActorContext:
    """Require a role permitted to view staff schedule data."""
    return require_staff_role(
        actor,
        (
            StaffRole.ADMIN,
            StaffRole.SCHEDULER,
            StaffRole.CLINICIAN,
        ),
    )
