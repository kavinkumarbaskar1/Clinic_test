"""Persistence data transfer models."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Provider:
    """Clinic provider record."""

    id: int
    display_name: str
    specialty: str | None
    active: bool
    created_at: str
    updated_at: str


@dataclass(frozen=True, slots=True)
class AppointmentType:
    """Appointment type with release-one eligibility flags."""

    id: int
    code: str
    name: str
    duration_minutes: int
    routine_eligible: bool
    standard_follow_up_eligible: bool
    excludes_new_patient_intake: bool
    excludes_urgent_care: bool
    excludes_emergency_care: bool
    active: bool
    created_at: str
    updated_at: str


@dataclass(frozen=True, slots=True)
class AvailabilitySlot:
    """Provider availability window."""

    id: int
    provider_id: int
    appointment_type_id: int | None
    starts_at: str
    ends_at: str
    status: str
    capacity: int
    created_at: str
    updated_at: str


@dataclass(frozen=True, slots=True)
class Appointment:
    """Booked appointment record."""

    id: int
    provider_id: int
    appointment_type_id: int
    availability_slot_id: int | None
    patient_reference: str
    starts_at: str
    ends_at: str
    status: str
    notes_reference: str | None
    created_at: str
    updated_at: str


@dataclass(frozen=True, slots=True)
class ReminderEvent:
    """Reminder delivery event."""

    id: int
    appointment_id: int
    channel: str
    scheduled_for: str
    status: str
    provider_event_id: str | None
    created_at: str
    updated_at: str


@dataclass(frozen=True, slots=True)
class AuditEvent:
    """Audit trail event."""

    id: int
    actor_reference: str | None
    action: str
    entity_type: str
    entity_id: int | None
    metadata_json: str
    created_at: str


@dataclass(frozen=True, slots=True)
class ConfigurationValue:
    """Application configuration value."""

    key: str
    value: str
    value_type: str
    is_secret: bool
    updated_at: str
