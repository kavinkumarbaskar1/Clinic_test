"""Audit service guardrail tests."""

import json
import sqlite3
import unittest
from pathlib import Path

from app.audit.service import (
    AuditEventRequest,
    AuditResourceReference,
    SensitiveAuditMetadataError,
    build_audit_metadata,
    record_audit_event,
)
from app.security.context import (
    RequestActorContext,
    StaffActorContext,
    StaffRole,
)


class AuditServiceTests(unittest.TestCase):
    """Verify audit events do not depend on sensitive message content."""

    def test_audit_metadata_does_not_require_phi_or_message_body(self) -> None:
        request = AuditEventRequest(
            event_type="appointment.booked",
            resource=AuditResourceReference(
                resource_type="appointment",
                resource_id=42,
                external_reference="appointment:42",
            ),
            metadata={"channel": "web"},
        )

        metadata = build_audit_metadata(request)

        self.assertEqual(metadata["resource_reference"], "appointment:42")
        self.assertEqual(metadata["channel"], "web")
        self.assertNotIn("phi", metadata)
        self.assertNotIn("message_body", metadata)
        self.assertNotIn("email_body", metadata)

    def test_audit_event_rejects_phi_and_email_message_body(self) -> None:
        request = AuditEventRequest(
            event_type="reminder.queued",
            resource=AuditResourceReference(resource_type="reminder_event"),
            metadata={
                "phi": "Patient diagnosis",
                "email_body": "Your appointment details are...",
            },
        )

        with self.assertRaises(SensitiveAuditMetadataError):
            build_audit_metadata(request)

    def test_record_audit_event_persists_sanitized_context(self) -> None:
        connection = sqlite3.connect(":memory:")
        connection.row_factory = sqlite3.Row
        try:
            initialize_database_for_connection(connection)
            request = AuditEventRequest(
                event_type="schedule.viewed",
                resource=AuditResourceReference(
                    resource_type="availability_slot",
                    resource_id=7,
                ),
                actor_context=RequestActorContext(
                    staff=StaffActorContext(
                        actor_reference="staff:user-123",
                        roles=frozenset({StaffRole.SCHEDULER}),
                    ),
                ),
                metadata={"view": "daily"},
            )

            event = record_audit_event(connection, request)
            stored_metadata = json.loads(event.metadata_json)

            self.assertEqual(event.actor_reference, "staff:user-123")
            self.assertEqual(event.action, "schedule.viewed")
            self.assertEqual(event.entity_type, "availability_slot")
            self.assertEqual(event.entity_id, 7)
            self.assertEqual(stored_metadata["view"], "daily")
            self.assertNotIn("message", stored_metadata)
            self.assertNotIn("patient_name", stored_metadata)
        finally:
            connection.close()


def initialize_database_for_connection(connection: sqlite3.Connection) -> None:
    """Apply the app's schema to an existing in-memory connection."""
    migration_path = (
        Path(__file__).resolve().parents[1]
        / "app"
        / "persistence"
        / "migrations"
        / "001_initial.sql"
    )
    connection.executescript(migration_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
