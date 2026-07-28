"""
TalentMind AI - Logging Configuration
=======================================
Structured logging setup with file rotation,
console output, and proper formatting.

Author  : TalentMind AI Team
Version : 1.0.0
"""

from __future__ import annotations

import logging
import logging.handlers
import sys
from pathlib import Path
from typing import Optional

from app.core.settings import get_settings


def setup_logging(
    log_level: Optional[str] = None,
    log_file: Optional[str] = None,
) -> logging.Logger:
    """
    Configures application-wide logging.

    Sets up:
    - Console handler with colored output
    - Rotating file handler
    - Structured log format

    Args:
        log_level: Override log level from settings
        log_file: Override log file path from settings

    Returns:
        logging.Logger: Configured root logger
    """
    cfg = get_settings()

    level_str  = log_level or cfg.LOG_LEVEL
    level      = getattr(logging, level_str.upper(), logging.INFO)
    file_path  = log_file or cfg.LOG_FILE

    # ── Log Format ──────────────────────────────────────────
    log_format = (
        "%(asctime)s | %(levelname)-8s | "
        "%(name)-30s | %(funcName)-25s | "
        "%(message)s"
    )
    date_format = "%Y-%m-%d %H:%M:%S"

    formatter = logging.Formatter(
        fmt=log_format,
        datefmt=date_format
    )

    # ── Root Logger ─────────────────────────────────────────
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    # Remove existing handlers to avoid duplicates
    root_logger.handlers.clear()

    # ── Console Handler ─────────────────────────────────────
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # ── File Handler (Rotating) ──────────────────────────────
    log_path = Path(file_path)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    file_handler = logging.handlers.RotatingFileHandler(
        filename=log_path,
        maxBytes=cfg.LOG_MAX_BYTES,
        backupCount=cfg.LOG_BACKUP_COUNT,
        encoding="utf-8",
    )
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)

    # ── Suppress noisy third-party loggers ──────────────────
    noisy_loggers = [
        "httpx", "httpcore", "urllib3",
        "google.auth", "google.api_core"
    ]
    for logger_name in noisy_loggers:
        logging.getLogger(logger_name).setLevel(logging.WARNING)

    root_logger.info(
        "Logging initialized | level=%s | file=%s",
        level_str, file_path
    )

    return root_logger


def get_logger(name: str) -> logging.Logger:
    """
    Returns a named logger for a module.

    Usage:
        logger = get_logger(__name__)
        logger.info("Message")

    Args:
        name: Logger name (typically __name__)

    Returns:
        logging.Logger: Named logger instance
    """
    return logging.getLogger(name)