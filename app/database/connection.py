"""
TalentMind AI - Database Connection Manager
=============================================
SQLAlchemy database connection with connection pooling,
session management, and health check capabilities.

Author  : TalentMind AI Team
Version : 1.0.0
"""

from __future__ import annotations

import logging
from contextlib import contextmanager
from pathlib import Path
from typing import Generator

from sqlalchemy import create_engine, event, text
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import (
    DeclarativeBase,
    Session,
    sessionmaker,
)

from app.core.settings import get_settings
from app.core.exceptions import DatabaseError

logger = logging.getLogger(__name__)


# ── Declarative Base ─────────────────────────────────────────
class Base(DeclarativeBase):
    """
    SQLAlchemy declarative base class.
    All ORM models must inherit from this class.
    """
    pass


# ── Database Manager ─────────────────────────────────────────
class DatabaseManager:
    """
    Manages database engine, sessions, and lifecycle.

    Implements singleton pattern to ensure a single
    engine instance throughout the application.

    Features:
        - Connection pooling
        - Automatic session cleanup
        - SQLite WAL mode for concurrency
        - Health check capability
        - Migration support
    """

    _instance: DatabaseManager | None = None
    _engine: Engine | None = None
    _session_factory: sessionmaker | None = None

    def __new__(cls) -> DatabaseManager:
        """Ensures singleton instance."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        """Initializes database manager (once)."""
        if self._engine is None:
            self._initialize()

    def _initialize(self) -> None:
        """
        Creates engine and session factory.
        Configures SQLite-specific optimizations.
        """
        cfg = get_settings()

        # Ensure database directory exists
        if cfg.DATABASE_URL.startswith("sqlite"):
            db_path = cfg.DATABASE_URL.replace(
                "sqlite:///", ""
            ).replace("sqlite://", "")
            Path(db_path).parent.mkdir(parents=True, exist_ok=True)

        # Create engine
        self._engine = create_engine(
            cfg.DATABASE_URL,
            echo=cfg.DATABASE_ECHO,
            connect_args={"check_same_thread": False}
            if "sqlite" in cfg.DATABASE_URL else {},
        )

        # SQLite-specific optimizations
        if "sqlite" in cfg.DATABASE_URL:
            @event.listens_for(self._engine, "connect")
            def set_sqlite_pragma(dbapi_conn, _):
                cursor = dbapi_conn.cursor()
                cursor.execute("PRAGMA journal_mode=WAL")
                cursor.execute("PRAGMA foreign_keys=ON")
                cursor.execute("PRAGMA synchronous=NORMAL")
                cursor.close()

        # Session factory
        self._session_factory = sessionmaker(
            bind=self._engine,
            autocommit=False,
            autoflush=False,
            expire_on_commit=False,
        )

        logger.info(
            "Database initialized | url=%s",
            cfg.DATABASE_URL
        )

    @property
    def engine(self) -> Engine:
        """Returns the SQLAlchemy engine."""
        if self._engine is None:
            raise DatabaseError("Database engine not initialized.")
        return self._engine

    def create_tables(self) -> None:
        """
        Creates all tables defined in ORM models.
        Safe to call multiple times (CREATE IF NOT EXISTS).
        """
        try:
            Base.metadata.create_all(bind=self._engine)
            logger.info("Database tables created successfully.")
        except SQLAlchemyError as exc:
            logger.error("Failed to create tables: %s", exc)
            raise DatabaseError(
                f"Table creation failed: {exc}"
            ) from exc

    def health_check(self) -> bool:
        """
        Verifies database connectivity.

        Returns:
            bool: True if connection is healthy, False otherwise
        """
        try:
            with self._engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return True
        except SQLAlchemyError as exc:
            logger.error("Database health check failed: %s", exc)
            return False

    @contextmanager
    def get_session(self) -> Generator[Session, None, None]:
        """
        Context manager that provides a database session.

        Handles:
        - Automatic commit on success
        - Automatic rollback on exception
        - Session cleanup on exit

        Yields:
            Session: SQLAlchemy session

        Example:
            with db.get_session() as session:
                session.add(record)
        """
        session: Session = self._session_factory()
        try:
            yield session
            session.commit()
        except SQLAlchemyError as exc:
            session.rollback()
            logger.error("Session error, rolling back: %s", exc)
            raise DatabaseError(
                f"Database operation failed: {exc}"
            ) from exc
        finally:
            session.close()

    def dispose(self) -> None:
        """Disposes the engine and cleans up connections."""
        if self._engine:
            self._engine.dispose()
            logger.info("Database engine disposed.")


# ── Module-level Instance ────────────────────────────────────
db_manager = DatabaseManager()