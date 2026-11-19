"""SQLite database setup utilities."""

import os
import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

MIGRATIONS_DIR = Path(__file__).resolve().parent / "migrations"
DEFAULT_DATABASE_PATH = Path("clinic_booking.sqlite3")


def get_database_path() -> Path:
    """Return the configured SQLite database path."""
    configured_path = os.environ.get("CLINIC_DATABASE_PATH")
    if configured_path:
        return Path(configured_path)
    return DEFAULT_DATABASE_PATH


def connect_database(
    database_path: str | Path | None = None,
) -> sqlite3.Connection:
    """Open a SQLite connection with application defaults."""
    path = (
        Path(database_path)
        if database_path is not None
        else get_database_path()
    )
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


@contextmanager
def database_connection(
    database_path: str | Path | None = None,
) -> Iterator[sqlite3.Connection]:
    """Yield a configured database connection and close it afterwards."""
    connection = connect_database(database_path)
    try:
        yield connection
    finally:
        connection.close()


@contextmanager
def transaction(
    connection: sqlite3.Connection,
) -> Iterator[sqlite3.Connection]:
    """Run a group of writes atomically."""
    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise


def initialize_database(database_path: str | Path | None = None) -> None:
    """Create baseline tables by applying idempotent migrations."""
    with database_connection(database_path) as connection:
        with transaction(connection):
            for migration_path in sorted(MIGRATIONS_DIR.glob("*.sql")):
                connection.executescript(migration_path.read_text(encoding="utf-8"))
