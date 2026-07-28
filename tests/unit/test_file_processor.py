"""
TalentMind AI - File Processor Unit Tests
==========================================
Tests for file processing pipeline.

Author  : TalentMind AI Team
Version : 1.0.0
"""

import pytest
from unittest.mock import MagicMock, patch
from pathlib import Path

from app.processors.file_processor import FileProcessor
from app.core.exceptions import (
    EmptyDocumentError,
    FileExtractionError,
    InvalidFileTypeError,
)


class TestFileProcessor:
    """Tests for FileProcessor class."""

    @pytest.fixture
    def processor(self):
        """Returns FileProcessor instance."""
        return FileProcessor()

    def test_clean_text_removes_null_bytes(self, processor):
        text   = "Hello\x00World"
        result = processor._clean_text(text)
        assert "\x00" not in result
        assert "Hello" in result
        assert "World" in result

    def test_clean_text_normalizes_whitespace(self, processor):
        text   = "Hello    World"
        result = processor._clean_text(text)
        assert "  " not in result

    def test_clean_text_removes_excessive_newlines(
        self, processor
    ):
        text   = "Line1\n\n\n\n\nLine2"
        result = processor._clean_text(text)
        assert "\n\n\n" not in result

    def test_clean_text_strips_whitespace(self, processor):
        text   = "   Hello World   "
        result = processor._clean_text(text)
        assert not result.startswith(" ")
        assert not result.endswith(" ")

    def test_extract_txt_reads_utf8(
        self, processor, tmp_path
    ):
        txt_file = tmp_path / "test.txt"
        content  = "This is a test resume content " * 10
        txt_file.write_text(content, encoding="utf-8")
        result = processor._extract_txt(
            txt_file, "test.txt"
        )
        assert "test resume content" in result

    def test_extract_txt_empty_raises(
        self, processor, tmp_path
    ):
        txt_file = tmp_path / "empty.txt"
        txt_file.write_text("", encoding="utf-8")
        with pytest.raises(FileExtractionError):
            processor._extract_txt(txt_file, "empty.txt")

    def test_save_file_creates_file(
        self, processor, tmp_path
    ):
        processor._upload_dir = tmp_path
        result = processor._save_file(
            b"test content", "test-id", "test.txt"
        )
        assert result.exists()
        assert result.read_bytes() == b"test content"

    def test_save_file_uses_uuid_prefix(
        self, processor, tmp_path
    ):
        processor._upload_dir = tmp_path
        result = processor._save_file(
            b"content", "my-uuid", "resume.pdf"
        )
        assert "my-uuid" in result.name

    def test_cleanup_removes_file(
        self, processor, tmp_path
    ):
        test_file = tmp_path / "test.txt"
        test_file.write_text("content")
        assert test_file.exists()
        processor.cleanup_file(str(test_file))
        assert not test_file.exists()

    def test_cleanup_nonexistent_file_no_error(
        self, processor
    ):
        # Should not raise
        processor.cleanup_file("/nonexistent/path.txt")


class TestTextCleaning:
    """Tests for text cleaning operations."""

    @pytest.fixture
    def processor(self):
        return FileProcessor()

    def test_normalize_line_endings(self, processor):
        text   = "Line1\r\nLine2\rLine3"
        result = processor._clean_text(text)
        assert "\r" not in result

    def test_strip_lines(self, processor):
        text   = "  Line1  \n  Line2  "
        result = processor._clean_text(text)
        for line in result.split("\n"):
            assert not line.startswith(" ")
            assert not line.endswith(" ")

    def test_preserves_content(self, processor):
        text   = "John Smith\nPython Developer\nEmail: john@test.com"
        result = processor._clean_text(text)
        assert "John Smith" in result
        assert "Python Developer" in result
        assert "john@test.com" in result
        