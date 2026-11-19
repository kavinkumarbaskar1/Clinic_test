"""Security context abstractions for staff-facing workflows."""

from dataclasses import dataclass, field
from enum import StrEnum


class StaffRole(StrEnum):
    """Recognized staff roles for future authorization checks."""

    ADMIN = "admin"
    SCHEDULER = "scheduler"
    CLINICIAN = "clinician"
    READ_ONLY = "read_only"


@dataclass(frozen=True, slots=True)
class StaffActorContext:
    """Provider-neutral staff identity context."""

    actor_reference: str
    roles: frozenset[StaffRole] = field(default_factory=frozenset)
    display_reference: str | None = None

    def has_role(self, required_role: StaffRole) -> bool:
        """Return whether this actor has a specific role."""
        return required_role in self.roles


@dataclass(frozen=True, slots=True)
class RequestActorContext:
    """Actor context for audit events and authorization boundaries."""

    staff: StaffActorContext | None = None
    patient_reference: str | None = None

    @property
    def audit_reference(self) -> str | None:
        """Return a non-sensitive reference suitable for audit records."""
        if self.staff is not None:
            return self.staff.actor_reference
        return self.patient_reference
