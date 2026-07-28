"""
TalentMind AI - Input Validators
==================================
Centralized validation functions with clear error
messages and type safety.

Author  : TalentMind AI Team
Version : 1.0.0
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Optional

from app.core.exceptions import (
    FileSizeExceededError,
    InvalidFileTypeError,
    ValidationError,
)
from app.core.settings import get_settings

cfg = get_settings()


def validate_file_type(file_name: str) -> str:
    """
    Validates file extension against allowed types.

    Args:
        file_name: Original file name with extension

    Returns:
        str: Validated file extension (lowercase)

    Raises:
        InvalidFileTypeError: If file type not supported
    """
    extension = Path(file_name).suffix.lower().lstrip(".")

    if not extension:
        raise InvalidFileTypeError(
            file_type="(no extension)",
            allowed_types=cfg.allowed_file_types_list
        )

    if extension not in cfg.allowed_file_types_list:
        raise InvalidFileTypeError(
            file_type=extension,
            allowed_types=cfg.allowed_file_types_list
        )

    return extension


def validate_file_size(
    file_size_bytes: int,
    max_size_mb: Optional[int] = None
) -> None:
    """
    Validates file size against maximum limit.

    Args:
        file_size_bytes: File size in bytes
        max_size_mb: Override max size (optional)

    Raises:
        FileSizeExceededError: If file exceeds limit
    """
    limit_mb = max_size_mb or cfg.MAX_FILE_SIZE_MB
    limit_bytes = limit_mb * 1024 * 1024
    file_size_mb = file_size_bytes / (1024 * 1024)

    if file_size_bytes > limit_bytes:
        raise FileSizeExceededError(
            file_size_mb=file_size_mb,
            max_size_mb=limit_mb
        )


def validate_email(email: str) -> str:
    """
    Validates email address format.

    Args:
        email: Email address string

    Returns:
        str: Normalized email address

    Raises:
        ValidationError: If email format is invalid
    """
    pattern = r"^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$"
    normalized = email.strip().lower()

    if not re.match(pattern, normalized):
        raise ValidationError(
            field="email",
            message=f"'{email}' is not a valid email address."
        )

    return normalized


def validate_text_content(
    text: str,
    field_name: str = "text",
    min_length: int = 100,
    max_length: int = 50_000
) -> str:
    """
    Validates extracted text content length and quality.

    Args:
        text: Text content to validate
        field_name: Field name for error messages
        min_length: Minimum required character count
        max_length: Maximum allowed character count

    Returns:
        str: Stripped text content

    Raises:
        ValidationError: If text fails validation
    """
    stripped = text.strip()

    if len(stripped) < min_length:
        raise ValidationError(
            field=field_name,
            message=(
                f"Content too short ({len(stripped)} chars). "
                f"Minimum required: {min_length} chars."
            )
        )

    if len(stripped) > max_length:
        raise ValidationError(
            field=field_name,
            message=(
                f"Content too long ({len(stripped)} chars). "
                f"Maximum allowed: {max_length} chars."
            )
        )

    return stripped


def sanitize_filename(filename: str) -> str:
    """
    Sanitizes a filename to remove dangerous characters
    including path traversal sequences.

    Args:
        filename: Original filename

    Returns:
        str: Safe filename string
    """
    # Step 1 - Get only the base filename (removes path)
    # This handles  ../../malicious.pdf  ->  malicious.pdf
    safe = Path(filename).name

    # Step 2 - Remove any remaining path traversal dots
    # Handles edge cases like  ..malicious.pdf
    while safe.startswith("."):
        safe = safe.lstrip(".")

    # Step 3 - Remove dangerous characters
    safe = re.sub(r'[<>:"/\\|?*\x00-\x1F]', "_", safe)

    # Step 4 - Remove any remaining double dots
    safe = safe.replace("..", "_")

    # Step 5 - Strip leading/trailing spaces and dots
    safe = safe.strip(". ")

    # Step 6 - Handle empty result
    if not safe:
        safe = "unnamed_file"

    # Step 7 - Limit filename length
    if len(safe) > 255:
        stem   = Path(safe).stem[:200]
        suffix = Path(safe).suffix
        safe   = f"{stem}{suffix}"

    return safe