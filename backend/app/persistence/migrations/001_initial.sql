PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS provider (
    id INTEGER PRIMARY KEY,
    display_name TEXT NOT NULL,
    specialty TEXT,
    active INTEGER NOT NULL DEFAULT 1 CHECK (active IN (0, 1)),
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS appointment_type (
    id INTEGER PRIMARY KEY,
    code TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    duration_minutes INTEGER NOT NULL CHECK (duration_minutes > 0),
    routine_eligible INTEGER NOT NULL DEFAULT 0
        CHECK (routine_eligible IN (0, 1)),
    standard_follow_up_eligible INTEGER NOT NULL DEFAULT 0
        CHECK (standard_follow_up_eligible IN (0, 1)),
    excludes_new_patient_intake INTEGER NOT NULL DEFAULT 0
        CHECK (excludes_new_patient_intake IN (0, 1)),
    excludes_urgent_care INTEGER NOT NULL DEFAULT 0
        CHECK (excludes_urgent_care IN (0, 1)),
    excludes_emergency_care INTEGER NOT NULL DEFAULT 0
        CHECK (excludes_emergency_care IN (0, 1)),
    active INTEGER NOT NULL DEFAULT 1 CHECK (active IN (0, 1)),
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS availability_slot (
    id INTEGER PRIMARY KEY,
    provider_id INTEGER NOT NULL,
    appointment_type_id INTEGER,
    starts_at TEXT NOT NULL,
    ends_at TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'open'
        CHECK (status IN ('open', 'held', 'booked', 'blocked')),
    capacity INTEGER NOT NULL DEFAULT 1 CHECK (capacity > 0),
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (provider_id) REFERENCES provider (id) ON DELETE CASCADE,
    FOREIGN KEY (appointment_type_id)
        REFERENCES appointment_type (id)
        ON DELETE SET NULL,
    UNIQUE (provider_id, starts_at, ends_at)
);

CREATE TABLE IF NOT EXISTS appointment (
    id INTEGER PRIMARY KEY,
    provider_id INTEGER NOT NULL,
    appointment_type_id INTEGER NOT NULL,
    availability_slot_id INTEGER,
    patient_reference TEXT NOT NULL,
    starts_at TEXT NOT NULL,
    ends_at TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'scheduled'
        CHECK (
            status IN (
                'scheduled',
                'cancelled',
                'completed',
                'no_show',
                'rescheduled'
            )
        ),
    notes_reference TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (provider_id) REFERENCES provider (id) ON DELETE RESTRICT,
    FOREIGN KEY (appointment_type_id)
        REFERENCES appointment_type (id)
        ON DELETE RESTRICT,
    FOREIGN KEY (availability_slot_id)
        REFERENCES availability_slot (id)
        ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS reminder_event (
    id INTEGER PRIMARY KEY,
    appointment_id INTEGER NOT NULL,
    channel TEXT NOT NULL CHECK (channel IN ('email', 'sms', 'phone')),
    scheduled_for TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending'
        CHECK (
            status IN (
                'pending',
                'sent',
                'failed',
                'cancelled',
                'skipped'
            )
        ),
    provider_event_id TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (appointment_id)
        REFERENCES appointment (id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS audit_event (
    id INTEGER PRIMARY KEY,
    actor_reference TEXT,
    action TEXT NOT NULL,
    entity_type TEXT NOT NULL,
    entity_id INTEGER,
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS configuration_value (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL,
    value_type TEXT NOT NULL DEFAULT 'string'
        CHECK (value_type IN ('string', 'integer', 'boolean', 'json')),
    is_secret INTEGER NOT NULL DEFAULT 0 CHECK (is_secret IN (0, 1)),
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
