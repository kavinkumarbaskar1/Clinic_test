"""Audit event helpers that avoid recording sensitive message content."""

from __future__ import annotations

import json
import sqlite3
from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

from app.persistence.models import AuditEvent
from app.persistence.repositories import ClinicRepository
from app.security.context import RequestActorContext

_DISALLOWED_METADATA_KEYS = frozenset(
    {
        "body",
        "content",
        "date_of_birth",
        "diagnosis",
        "email_body",
        "email_message",
        "message",
        "message_body",
        "patient_name",
        "phone",
        "phi",
        "ssn",
        "token",
    },
)


@dataclass(frozen=True, slots=True)
class AuditResourceReference:
    """Non-sensitive reference to the resource involved in an event."""

    resource_type: str
    resource_id: int | None = None
    external_reference: str | None = None


@dataclass(frozen=True, slots=True)
class AuditEventRequest:
    """Sanitized audit event request accepted by the audit service."""

    event_type: str
    resource: AuditResourceReference
    actor_context: RequestActorContext | None = None
    metadata: Mapping[str, str | int | bool | None] = field(
        default_factory=dict,
    )
    occurred_at: datetime = field(default_factory=lambda: datetime.now(UTC))


class SensitiveAuditMetadataError(ValueError):
    """Raised when audit metadata includes content that must not be stored."""


def build_audit_metadata(request: AuditEventRequest) -> dict[str, Any]:
    """Build audit metadata with event time and non-sensitive references."""
    _validate_metadata(request.metadata)
    metadata: dict[str, Any] = {
        "occurred_at": request.occurred_at.isoformat(),
    }
    if request.resource.external_reference is not None:
        metadata["resource_reference"] = request.resource.external_reference
    metadata.update(request.metadata)
    return metadata


def record_audit_event(
    connection: sqlite3.Connection,
    request: AuditEventRequest,
) -> AuditEvent:
    """Persist an audit event without storing sensitive content."""
    repository = ClinicRepository(connection)
    metadata_json = json.dumps(
        build_audit_metadata(request),
        sort_keys=True,
        separators=(",", ":"),
    )
    actor_reference = (
        request.actor_context.audit_reference
        if request.actor_context is not None
        else None
    )
    return repository.create_audit_event(
        action=request.event_type,
        entity_type=request.resource.resource_type,
        actor_reference=actor_reference,
        entity_id=request.resource.resource_id,
        metadata_json=metadata_json,
    )


def _validate_metadata(
    metadata: Mapping[str, str | int | bool | None],
) -> None:
    disallowed = _DISALLOWED_METADATA_KEYS.intersection(metadata.keys())
    if disallowed:
        names = ", ".join(sorted(disallowed))
        raise SensitiveAuditMetadataError(
            f"Audit metadata cannot include sensitive fields: {names}",
        )
