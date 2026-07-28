"""
TalentMind AI - Custom Exceptions
===================================
Defines all application-specific exceptions with
proper hierarchy for structured error handling.

Author  : TalentMind AI Team
Version : 1.0.0
"""

from __future__ import annotations
from typing import Optional, Dict, Any


class TalentMindBaseException(Exception):
    """
    Base exception for all TalentMind AI exceptions.

    All custom exceptions should inherit from this class
    to enable consistent error handling and logging.
    """

    def __init__(
        self,
        message: str,
        error_code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.message = message
        self.error_code = error_code or "TALENTMIND_ERROR"
        self.details = details or {}
        super().__init__(self.message)

    def to_dict(self) -> Dict[str, Any]:
        """Converts exception to dictionary for API responses."""
        return {
            "error": self.error_code,
            "message": self.message,
            "details": self.details,
        }

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"code={self.error_code!r}, "
            f"message={self.message!r})"
        )


# ── Configuration Exceptions ─────────────────────────────────

class ConfigurationError(TalentMindBaseException):
    """Raised when application configuration is invalid."""

    def __init__(self, message: str, **kwargs: Any) -> None:
        super().__init__(
            message=message,
            error_code="CONFIG_ERROR",
            **kwargs
        )


class APIKeyNotConfiguredError(ConfigurationError):
    """Raised when required API key is missing or invalid."""

    def __init__(self, service: str = "Google Gemini") -> None:
        super().__init__(
            message=(
                f"{service} API key is not configured. "
                f"Please set it in your .env file."
            ),
            details={"service": service}
        )
        self.error_code = "API_KEY_MISSING"


# ── File Processing Exceptions ───────────────────────────────

class FileProcessingError(TalentMindBaseException):
    """Base exception for file processing errors."""

    def __init__(self, message: str, **kwargs: Any) -> None:
        super().__init__(
            message=message,
            error_code="FILE_PROCESSING_ERROR",
            **kwargs
        )


class InvalidFileTypeError(FileProcessingError):
    """Raised when uploaded file type is not supported."""

    def __init__(
        self,
        file_type: str,
        allowed_types: list
    ) -> None:
        super().__init__(
            message=(
                f"File type '{file_type}' is not supported. "
                f"Allowed types: {', '.join(allowed_types)}"
            ),
            details={
                "file_type": file_type,
                "allowed_types": allowed_types
            }
        )
        self.error_code = "INVALID_FILE_TYPE"


class FileSizeExceededError(FileProcessingError):
    """Raised when uploaded file exceeds size limit."""

    def __init__(
        self,
        file_size_mb: float,
        max_size_mb: int
    ) -> None:
        super().__init__(
            message=(
                f"File size {file_size_mb:.1f}MB exceeds "
                f"the maximum allowed size of {max_size_mb}MB."
            ),
            details={
                "file_size_mb": file_size_mb,
                "max_size_mb": max_size_mb
            }
        )
        self.error_code = "FILE_SIZE_EXCEEDED"


class FileExtractionError(FileProcessingError):
    """Raised when text extraction from file fails."""

    def __init__(
        self,
        file_name: str,
        reason: str = "Unknown error"
    ) -> None:
        super().__init__(
            message=(
                f"Failed to extract text from '{file_name}'. "
                f"Reason: {reason}"
            ),
            details={"file_name": file_name, "reason": reason}
        )
        self.error_code = "EXTRACTION_FAILED"


class EmptyDocumentError(FileProcessingError):
    """Raised when extracted document has no content."""

    def __init__(self, file_name: str) -> None:
        super().__init__(
            message=(
                f"Document '{file_name}' appears to be empty "
                f"or contains no extractable text."
            ),
            details={"file_name": file_name}
        )
        self.error_code = "EMPTY_DOCUMENT"


# ── Agent Exceptions ─────────────────────────────────────────

class AgentError(TalentMindBaseException):
    """Base exception for AI agent errors."""

    def __init__(
        self,
        agent_name: str,
        message: str,
        **kwargs: Any
    ) -> None:
        super().__init__(
            message=f"[{agent_name}] {message}",
            error_code="AGENT_ERROR",
            details={"agent_name": agent_name},
            **kwargs
        )


class AgentTimeoutError(AgentError):
    """Raised when an agent operation times out."""

    def __init__(
        self,
        agent_name: str,
        timeout_seconds: int
    ) -> None:
        super().__init__(
            agent_name=agent_name,
            message=(
                f"Agent timed out after {timeout_seconds} seconds."
            )
        )
        self.error_code = "AGENT_TIMEOUT"


class AgentResponseError(AgentError):
    """Raised when agent receives invalid response from LLM."""

    def __init__(
        self,
        agent_name: str,
        response: str = ""
    ) -> None:
        super().__init__(
            agent_name=agent_name,
            message="Agent received an invalid or malformed response."
        )
        self.error_code = "AGENT_RESPONSE_ERROR"
        self.details["raw_response"] = response[:200]


# ── Database Exceptions ──────────────────────────────────────

class DatabaseError(TalentMindBaseException):
    """Base exception for database errors."""

    def __init__(self, message: str, **kwargs: Any) -> None:
        super().__init__(
            message=message,
            error_code="DATABASE_ERROR",
            **kwargs
        )


class RecordNotFoundError(DatabaseError):
    """Raised when a database record is not found."""

    def __init__(self, model: str, identifier: Any) -> None:
        super().__init__(
            message=(
                f"{model} with identifier '{identifier}' not found."
            ),
            details={"model": model, "identifier": str(identifier)}
        )
        self.error_code = "RECORD_NOT_FOUND"


# ── Validation Exceptions ────────────────────────────────────

class ValidationError(TalentMindBaseException):
    """Raised when input validation fails."""

    def __init__(
        self,
        field: str,
        message: str,
        **kwargs: Any
    ) -> None:
        super().__init__(
            message=f"Validation failed for '{field}': {message}",
            error_code="VALIDATION_ERROR",
            details={"field": field},
            **kwargs
        )