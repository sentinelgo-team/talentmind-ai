"""
TalentMind AI - File Processor
================================
Handles file type detection, routing to correct
extractor, and text cleaning pipeline.

Author  : TalentMind AI Team
Version : 1.0.0
"""

from __future__ import annotations

import logging
import os
import uuid
from pathlib import Path
from typing import Optional

from app.core.exceptions import (
    EmptyDocumentError,
    FileExtractionError,
    InvalidFileTypeError,
)
from app.core.settings import get_settings
from app.utils.validators import (
    sanitize_filename,
    validate_file_size,
    validate_file_type,
    validate_text_content,
)

logger = logging.getLogger(__name__)
cfg    = get_settings()


class FileProcessor:
    """
    Central file processing coordinator.

    Responsibilities:
        - Validate uploaded files
        - Route to correct extractor
        - Clean extracted text
        - Save files to disk
        - Return structured results

    Why needed:
        Separates file handling concerns from
        agent logic. Single entry point for all
        file operations ensures consistent
        validation and error handling.
    """

    def __init__(self) -> None:
        self._upload_dir = cfg.upload_dir_path
        self._upload_dir.mkdir(parents=True, exist_ok=True)

    def process(
        self,
        file_bytes: bytes,
        file_name: str,
    ) -> dict:
        """
        Full file processing pipeline.

        Steps:
            1. Validate file type
            2. Validate file size
            3. Save to disk
            4. Extract text
            5. Clean text
            6. Validate content

        Args:
            file_bytes : Raw file bytes from upload
            file_name  : Original filename

        Returns:
            dict: {
                file_id    : Unique file identifier
                file_name  : Sanitized filename
                file_type  : Extension (pdf/docx/txt)
                file_path  : Saved file path
                raw_text   : Extracted text
                char_count : Character count
            }

        Raises:
            InvalidFileTypeError   : Unsupported type
            FileSizeExceededError  : File too large
            FileExtractionError    : Extraction failed
            EmptyDocumentError     : No content found
        """
        logger.info(
            "Processing file | name=%s | size=%d bytes",
            file_name, len(file_bytes)
        )

        # Step 1 — Validate file type
        file_type = validate_file_type(file_name)

        # Step 2 — Validate file size
        validate_file_size(len(file_bytes))

        # Step 3 — Save to disk
        file_id    = str(uuid.uuid4())
        safe_name  = sanitize_filename(file_name)
        saved_path = self._save_file(
            file_bytes, file_id, safe_name
        )

        # Step 4 — Extract text
        raw_text = self._extract_text(
            saved_path, file_type, safe_name
        )

        # Step 5 — Clean text
        cleaned_text = self._clean_text(raw_text)

        # Step 6 — Validate content
        validate_text_content(
            cleaned_text,
            field_name="resume_content"
        )

        logger.info(
            "File processed | id=%s | chars=%d",
            file_id, len(cleaned_text)
        )

        return {
            "file_id"    : file_id,
            "file_name"  : safe_name,
            "file_type"  : file_type,
            "file_path"  : str(saved_path),
            "raw_text"   : cleaned_text,
            "char_count" : len(cleaned_text),
        }

    def process_file(self, file_path: str) -> dict:
        """
        Process a resume file from a path on disk.

        Args:
            file_path: Path to the file on disk

        Returns:
            dict: {
                success   : Whether processing succeeded
                text      : Extracted text content
                file_info : Metadata about the file
                error     : Error message if failed
            }
        """
        path = Path(file_path)
        try:
            file_bytes = path.read_bytes()
            result = self.process(file_bytes, path.name)
            return {
                "success": True,
                "text": result["raw_text"],
                "file_info": {
                    "file_id": result["file_id"],
                    "file_name": result["file_name"],
                    "file_type": result["file_type"],
                    "char_count": result["char_count"],
                },
                "error": None,
            }
        except Exception as exc:
            logger.error("process_file failed | path=%s | error=%s", file_path, exc)
            return {
                "success": False,
                "text": "",
                "file_info": {},
                "error": str(exc),
            }

    def _save_file(
        self,
        file_bytes : bytes,
        file_id    : str,
        file_name  : str,
    ) -> Path:
        """
        Saves uploaded file to disk with unique ID prefix.

        Args:
            file_bytes : Raw bytes
            file_id    : Unique identifier
            file_name  : Sanitized name

        Returns:
            Path: Saved file path
        """
        save_path = self._upload_dir / f"{file_id}_{file_name}"

        try:
            save_path.write_bytes(file_bytes)
            logger.debug("File saved | path=%s", save_path)
            return save_path

        except OSError as exc:
            raise FileExtractionError(
                file_name=file_name,
                reason=f"Could not save file: {exc}"
            ) from exc

    def _extract_text(
        self,
        file_path : Path,
        file_type : str,
        file_name : str,
    ) -> str:
        """
        Routes to correct extractor based on file type.

        Args:
            file_path : Path to saved file
            file_type : File extension
            file_name : Original name for errors

        Returns:
            str: Extracted raw text
        """
        extractors = {
            "pdf"  : self._extract_pdf,
            "docx" : self._extract_docx,
            "txt"  : self._extract_txt,
        }

        extractor = extractors.get(file_type)
        if not extractor:
            raise InvalidFileTypeError(
                file_type=file_type,
                allowed_types=cfg.allowed_file_types_list
            )

        return extractor(file_path, file_name)

    def _extract_pdf(
        self,
        file_path : Path,
        file_name : str,
    ) -> str:
        """
        Extracts text from PDF using PyPDF.

        Args:
            file_path : Path to PDF file
            file_name : Filename for error context

        Returns:
            str: Extracted text from all pages
        """
        try:
            from pypdf import PdfReader

            reader = PdfReader(str(file_path))
            pages  = []

            for page_num, page in enumerate(reader.pages, 1):
                page_text = page.extract_text()
                if page_text:
                    pages.append(page_text)
                    logger.debug(
                        "PDF page %d extracted | chars=%d",
                        page_num, len(page_text)
                    )

            if not pages:
                raise EmptyDocumentError(file_name=file_name)

            text = "\n".join(pages)
            logger.info(
                "PDF extracted | pages=%d | chars=%d",
                len(pages), len(text)
            )
            return text

        except EmptyDocumentError:
            raise
        except Exception as exc:
            raise FileExtractionError(
                file_name=file_name,
                reason=f"PDF extraction failed: {exc}"
            ) from exc

    def _extract_docx(
        self,
        file_path : Path,
        file_name : str,
    ) -> str:
        """
        Extracts text from DOCX using python-docx.

        Args:
            file_path : Path to DOCX file
            file_name : Filename for error context

        Returns:
            str: Extracted text from all paragraphs
        """
        try:
            from docx import Document

            doc        = Document(str(file_path))
            paragraphs = []

            for para in doc.paragraphs:
                text = para.text.strip()
                if text:
                    paragraphs.append(text)

            if not paragraphs:
                raise EmptyDocumentError(file_name=file_name)

            text = "\n".join(paragraphs)
            logger.info(
                "DOCX extracted | paragraphs=%d | chars=%d",
                len(paragraphs), len(text)
            )
            return text

        except EmptyDocumentError:
            raise
        except Exception as exc:
            raise FileExtractionError(
                file_name=file_name,
                reason=f"DOCX extraction failed: {exc}"
            ) from exc

    def _extract_txt(
        self,
        file_path : Path,
        file_name : str,
    ) -> str:
        """
        Extracts text from plain TXT file.

        Args:
            file_path : Path to TXT file
            file_name : Filename for error context

        Returns:
            str: File text content
        """
        encodings = ["utf-8", "utf-16", "latin-1", "cp1252"]

        for encoding in encodings:
            try:
                text = file_path.read_text(encoding=encoding)
                if text.strip():
                    logger.info(
                        "TXT extracted | encoding=%s | chars=%d",
                        encoding, len(text)
                    )
                    return text
            except (UnicodeDecodeError, UnicodeError):
                continue

        raise FileExtractionError(
            file_name=file_name,
            reason="Could not decode text file with any encoding."
        )

    def _clean_text(self, text: str) -> str:
        """
        Cleans and normalizes extracted text.

        Operations:
            - Remove null bytes
            - Normalize whitespace
            - Remove excessive blank lines
            - Strip leading/trailing whitespace

        Args:
            text: Raw extracted text

        Returns:
            str: Cleaned text
        """
        import re

        # Remove null bytes and control characters
        text = text.replace("\x00", " ")
        text = re.sub(r"[\x01-\x08\x0b\x0c\x0e-\x1f\x7f]", " ", text)

        # Normalize line endings
        text = text.replace("\r\n", "\n").replace("\r", "\n")

        # Remove excessive blank lines (max 2 consecutive)
        text = re.sub(r"\n{3,}", "\n\n", text)

        # Normalize spaces (multiple spaces to single)
        text = re.sub(r"[ \t]+", " ", text)

        # Strip each line
        lines = [line.strip() for line in text.split("\n")]
        text  = "\n".join(lines)

        return text.strip()

    def cleanup_file(self, file_path: str) -> None:
        """
        Removes a temporary uploaded file.

        Args:
            file_path: Path to file to delete
        """
        try:
            path = Path(file_path)
            if path.exists():
                path.unlink()
                logger.debug("Temp file removed | path=%s", file_path)
        except OSError as exc:
            logger.warning(
                "Could not remove temp file | path=%s | error=%s",
                file_path, exc
            )