"""Repository helpers for appointment persistence."""

import sqlite3

from app.persistence.models import (
    Appointment,
    AppointmentType,
    AuditEvent,
    AvailabilitySlot,
    ConfigurationValue,
    Provider,
    ReminderEvent,
)


def _as_bool(value: int) -> bool:
    return bool(value)


class ClinicRepository:
    """SQLite repository for baseline clinic booking records."""

    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

    def create_provider(
        self,
        display_name: str,
        specialty: str | None = None,
        active: bool = True,
    ) -> Provider:
        """Create and return a provider."""
        cursor = self._connection.execute(
            """
            INSERT INTO provider (display_name, specialty, active)
            VALUES (?, ?, ?)
            """,
            (display_name, specialty, int(active)),
        )
        return self.get_provider(cursor.lastrowid)

    def get_provider(self, provider_id: int) -> Provider:
        """Return a provider by identifier."""
        row = self._connection.execute(
            "SELECT * FROM provider WHERE id = ?",
            (provider_id,),
        ).fetchone()
        if row is None:
            raise LookupError("provider not found")
        return self._provider_from_row(row)

    def create_appointment_type(
        self,
        code: str,
        name: str,
        duration_minutes: int,
        routine_eligible: bool = False,
        standard_follow_up_eligible: bool = False,
        excludes_new_patient_intake: bool = False,
        excludes_urgent_care: bool = False,
        excludes_emergency_care: bool = False,
        active: bool = True,
    ) -> AppointmentType:
        """Create and return an appointment type."""
        cursor = self._connection.execute(
            """
            INSERT INTO appointment_type (
                code,
                name,
                duration_minutes,
                routine_eligible,
                standard_follow_up_eligible,
                excludes_new_patient_intake,
                excludes_urgent_care,
                excludes_emergency_care,
                active
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                code,
                name,
                duration_minutes,
                int(routine_eligible),
                int(standard_follow_up_eligible),
                int(excludes_new_patient_intake),
                int(excludes_urgent_care),
                int(excludes_emergency_care),
                int(active),
            ),
        )
        return self.get_appointment_type(cursor.lastrowid)

    def get_appointment_type(
        self,
        appointment_type_id: int,
    ) -> AppointmentType:
        """Return an appointment type by identifier."""
        row = self._connection.execute(
            "SELECT * FROM appointment_type WHERE id = ?",
            (appointment_type_id,),
        ).fetchone()
        if row is None:
            raise LookupError("appointment type not found")
        return self._appointment_type_from_row(row)

    def create_availability_slot(
        self,
        provider_id: int,
        starts_at: str,
        ends_at: str,
        appointment_type_id: int | None = None,
        status: str = "open",
        capacity: int = 1,
    ) -> AvailabilitySlot:
        """Create and return an availability slot."""
        cursor = self._connection.execute(
            """
            INSERT INTO availability_slot (
                provider_id,
                appointment_type_id,
                starts_at,
                ends_at,
                status,
                capacity
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                provider_id,
                appointment_type_id,
                starts_at,
                ends_at,
                status,
                capacity,
            ),
        )
        return self.get_availability_slot(cursor.lastrowid)

    def get_availability_slot(self, slot_id: int) -> AvailabilitySlot:
        """Return an availability slot by identifier."""
        row = self._connection.execute(
            "SELECT * FROM availability_slot WHERE id = ?",
            (slot_id,),
        ).fetchone()
        if row is None:
            raise LookupError("availability slot not found")
        return self._availability_slot_from_row(row)

    def create_appointment(
        self,
        provider_id: int,
        appointment_type_id: int,
        patient_reference: str,
        starts_at: str,
        ends_at: str,
        availability_slot_id: int | None = None,
        status: str = "scheduled",
        notes_reference: str | None = None,
    ) -> Appointment:
        """Create and return an appointment."""
        cursor = self._connection.execute(
            """
            INSERT INTO appointment (
                provider_id,
                appointment_type_id,
                availability_slot_id,
                patient_reference,
                starts_at,
                ends_at,
                status,
                notes_reference
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                provider_id,
                appointment_type_id,
                availability_slot_id,
                patient_reference,
                starts_at,
                ends_at,
                status,
                notes_reference,
            ),
        )
        return self.get_appointment(cursor.lastrowid)

    def get_appointment(self, appointment_id: int) -> Appointment:
        """Return an appointment by identifier."""
        row = self._connection.execute(
            "SELECT * FROM appointment WHERE id = ?",
            (appointment_id,),
        ).fetchone()
        if row is None:
            raise LookupError("appointment not found")
        return self._appointment_from_row(row)

    def create_reminder_event(
        self,
        appointment_id: int,
        channel: str,
        scheduled_for: str,
        status: str = "pending",
        provider_event_id: str | None = None,
    ) -> ReminderEvent:
        """Create and return a reminder event."""
        cursor = self._connection.execute(
            """
            INSERT INTO reminder_event (
                appointment_id,
                channel,
                scheduled_for,
                status,
                provider_event_id
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                appointment_id,
                channel,
                scheduled_for,
                status,
                provider_event_id,
            ),
        )
        return self.get_reminder_event(cursor.lastrowid)

    def get_reminder_event(self, reminder_event_id: int) -> ReminderEvent:
        """Return a reminder event by identifier."""
        row = self._connection.execute(
            "SELECT * FROM reminder_event WHERE id = ?",
            (reminder_event_id,),
        ).fetchone()
        if row is None:
            raise LookupError("reminder event not found")
        return self._reminder_event_from_row(row)

    def create_audit_event(
        self,
        action: str,
        entity_type: str,
        actor_reference: str | None = None,
        entity_id: int | None = None,
        metadata_json: str = "{}",
    ) -> AuditEvent:
        """Create and return an audit event."""
        cursor = self._connection.execute(
            """
            INSERT INTO audit_event (
                actor_reference,
                action,
                entity_type,
                entity_id,
                metadata_json
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                actor_reference,
                action,
                entity_type,
                entity_id,
                metadata_json,
            ),
        )
        return self.get_audit_event(cursor.lastrowid)

    def get_audit_event(self, audit_event_id: int) -> AuditEvent:
        """Return an audit event by identifier."""
        row = self._connection.execute(
            "SELECT * FROM audit_event WHERE id = ?",
            (audit_event_id,),
        ).fetchone()
        if row is None:
            raise LookupError("audit event not found")
        return self._audit_event_from_row(row)

    def set_configuration_value(
        self,
        key: str,
        value: str,
        value_type: str = "string",
        is_secret: bool = False,
    ) -> ConfigurationValue:
        """Create or update a configuration value."""
        self._connection.execute(
            """
            INSERT INTO configuration_value (
                key,
                value,
                value_type,
                is_secret
            )
            VALUES (?, ?, ?, ?)
            ON CONFLICT(key) DO UPDATE SET
                value = excluded.value,
                value_type = excluded.value_type,
                is_secret = excluded.is_secret,
                updated_at = CURRENT_TIMESTAMP
            """,
            (key, value, value_type, int(is_secret)),
        )
        return self.get_configuration_value(key)

    def get_configuration_value(self, key: str) -> ConfigurationValue:
        """Return a configuration value by key."""
        row = self._connection.execute(
            "SELECT * FROM configuration_value WHERE key = ?",
            (key,),
        ).fetchone()
        if row is None:
            raise LookupError("configuration value not found")
        return self._configuration_value_from_row(row)

    @staticmethod
    def _provider_from_row(row: sqlite3.Row) -> Provider:
        return Provider(
            id=row["id"],
            display_name=row["display_name"],
            specialty=row["specialty"],
            active=_as_bool(row["active"]),
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

    @staticmethod
    def _appointment_type_from_row(row: sqlite3.Row) -> AppointmentType:
        return AppointmentType(
            id=row["id"],
            code=row["code"],
            name=row["name"],
            duration_minutes=row["duration_minutes"],
            routine_eligible=_as_bool(row["routine_eligible"]),
            standard_follow_up_eligible=_as_bool(
                row["standard_follow_up_eligible"],
            ),
            excludes_new_patient_intake=_as_bool(
                row["excludes_new_patient_intake"],
            ),
            excludes_urgent_care=_as_bool(row["excludes_urgent_care"]),
            excludes_emergency_care=_as_bool(row["excludes_emergency_care"]),
            active=_as_bool(row["active"]),
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

    @staticmethod
    def _availability_slot_from_row(row: sqlite3.Row) -> AvailabilitySlot:
        return AvailabilitySlot(
            id=row["id"],
            provider_id=row["provider_id"],
            appointment_type_id=row["appointment_type_id"],
            starts_at=row["starts_at"],
            ends_at=row["ends_at"],
            status=row["status"],
            capacity=row["capacity"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

    @staticmethod
    def _appointment_from_row(row: sqlite3.Row) -> Appointment:
        return Appointment(
            id=row["id"],
            provider_id=row["provider_id"],
            appointment_type_id=row["appointment_type_id"],
            availability_slot_id=row["availability_slot_id"],
            patient_reference=row["patient_reference"],
            starts_at=row["starts_at"],
            ends_at=row["ends_at"],
            status=row["status"],
            notes_reference=row["notes_reference"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

    @staticmethod
    def _reminder_event_from_row(row: sqlite3.Row) -> ReminderEvent:
        return ReminderEvent(
            id=row["id"],
            appointment_id=row["appointment_id"],
            channel=row["channel"],
            scheduled_for=row["scheduled_for"],
            status=row["status"],
            provider_event_id=row["provider_event_id"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

    @staticmethod
    def _audit_event_from_row(row: sqlite3.Row) -> AuditEvent:
        return AuditEvent(
            id=row["id"],
            actor_reference=row["actor_reference"],
            action=row["action"],
            entity_type=row["entity_type"],
            entity_id=row["entity_id"],
            metadata_json=row["metadata_json"],
            created_at=row["created_at"],
        )

    @staticmethod
    def _configuration_value_from_row(row: sqlite3.Row) -> ConfigurationValue:
        return ConfigurationValue(
            key=row["key"],
            value=row["value"],
            value_type=row["value_type"],
            is_secret=_as_bool(row["is_secret"]),
            updated_at=row["updated_at"],
        )
