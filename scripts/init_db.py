"""
TalentMind AI - Database Initialization Script
================================================
Run this script once to create all database tables
and seed initial data.

Usage:
    python scripts/init_db.py

Author  : TalentMind AI Team
Version : 1.0.0
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import logging
from app.core.logging_config import setup_logging
from app.core.settings import get_settings
from app.database.connection import db_manager
from app.database import models  # noqa: F401 — registers models


def initialize_database() -> None:
    """
    Initializes the database by:
    1. Running health check
    2. Creating all tables
    3. Logging success/failure
    """
    logger = setup_logging()
    cfg = get_settings()

    logger.info("=" * 60)
    logger.info("TalentMind AI  ─  Database Initialization")
    logger.info("=" * 60)
    logger.info("Database URL : %s", cfg.DATABASE_URL)
    logger.info("Environment  : %s", cfg.APP_ENV)

    # Health check
    logger.info("Running database health check...")
    if not db_manager.health_check():
        logger.error("Database health check FAILED.")
        sys.exit(1)
    logger.info("Database health check PASSED.")

    # Create tables
    logger.info("Creating database tables...")
    try:
        db_manager.create_tables()
        logger.info("All tables created successfully.")
    except Exception as exc:
        logger.error("Table creation FAILED: %s", exc)
        sys.exit(1)

    logger.info("=" * 60)
    logger.info("Database initialization COMPLETE.")
    logger.info("=" * 60)


if __name__ == "__main__":
    initialize_database()