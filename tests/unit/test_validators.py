"""
TalentMind AI - Validator Unit Tests
======================================
Tests for all input validation functions.

Author  : TalentMind AI Team
Version : 1.0.0
"""

import pytest
from app.utils.validators import (
    validate_file_type,
    validate_file_size,
    validate_email,
    validate_text_content,
    sanitize_filename,
)
from app.core.exceptions import (
    InvalidFileTypeError,
    FileSizeExceededError,
    ValidationError,
)


class TestFileTypeValidator:
    """Tests for validate_file_type()"""

    def test_valid_pdf(self):
        assert validate_file_type("resume.pdf") == "pdf"

    def test_valid_docx(self):
        assert validate_file_type("resume.docx") == "docx"

    def test_valid_txt(self):
        assert validate_file_type("resume.txt") == "txt"

    def test_uppercase_extension(self):
        assert validate_file_type("RESUME.PDF") == "pdf"

    def test_invalid_exe(self):
        with pytest.raises(InvalidFileTypeError):
            validate_file_type("malware.exe")

    def test_invalid_js(self):
        with pytest.raises(InvalidFileTypeError):
            validate_file_type("script.js")

    def test_no_extension(self):
        with pytest.raises(InvalidFileTypeError):
            validate_file_type("resumefile")


class TestFileSizeValidator:
    """Tests for validate_file_size()"""

    def test_valid_small_file(self):
        validate_file_size(1024)  # 1 KB - should pass

    def test_valid_max_file(self):
        validate_file_size(9 * 1024 * 1024)  # 9 MB

    def test_exceeds_limit(self):
        with pytest.raises(FileSizeExceededError):
            validate_file_size(15 * 1024 * 1024)  # 15 MB

    def test_custom_limit(self):
        with pytest.raises(FileSizeExceededError):
            validate_file_size(3 * 1024 * 1024, max_size_mb=2)

    def test_zero_bytes(self):
        validate_file_size(0)  # Should pass (handled elsewhere)


class TestEmailValidator:
    """Tests for validate_email()"""

    def test_valid_email(self):
        assert validate_email("user@example.com") == "user@example.com"

    def test_normalizes_to_lowercase(self):
        assert validate_email("User@Example.COM") == "user@example.com"

    def test_valid_complex_email(self):
        result = validate_email("user.name+tag@domain.co.uk")
        assert result == "user.name+tag@domain.co.uk"

    def test_invalid_no_at(self):
        with pytest.raises(ValidationError):
            validate_email("userexample.com")

    def test_invalid_no_domain(self):
        with pytest.raises(ValidationError):
            validate_email("user@")

    def test_invalid_spaces(self):
        with pytest.raises(ValidationError):
            validate_email("user @example.com")


class TestTextValidator:
    """Tests for validate_text_content()"""

    def test_valid_text(self):
        text = "A" * 500
        result = validate_text_content(text)
        assert result == text

    def test_too_short(self):
        with pytest.raises(ValidationError):
            validate_text_content("Short text")

    def test_exactly_minimum(self):
        text = "A" * 100
        validate_text_content(text)  # Should not raise

    def test_strips_whitespace(self):
        text = "   " + ("A" * 200) + "   "
        result = validate_text_content(text)
        assert not result.startswith(" ")
        assert not result.endswith(" ")

    def test_too_long(self):
        with pytest.raises(ValidationError):
            validate_text_content("A" * 60_000)


class TestSanitizeFilename:
    """Tests for sanitize_filename()"""

    def test_normal_filename(self):
        assert sanitize_filename("resume.pdf") == "resume.pdf"

    def test_removes_path_traversal(self):
        result = sanitize_filename("../../malicious.pdf")
        assert ".." not in result

    def test_removes_special_chars(self):
        result = sanitize_filename('file<>:"/\\|?*.pdf')
        assert "<" not in result
        assert ">" not in result

    def test_empty_string(self):
        result = sanitize_filename("")
        assert result == "unnamed_file"

    def test_very_long_name(self):
        long_name = "a" * 300 + ".pdf"
        result = sanitize_filename(long_name)
        assert len(result) <= 255