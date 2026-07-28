"""
TalentMind AI - Resume Parser Service
========================================
Purpose: Service layer for resume parsing operations.
         Bridges UI pages with ResumeAgent.

Author  : TalentMind AI Team
Version : 1.0.0
"""

from __future__ import annotations

import logging
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


class ResumeParser:
    """
    Service class for resume parsing operations.

    Orchestrates file processing and resume agent
    to extract structured data from resumes.

    Usage:
        parser = ResumeParser()
        result = parser.parse(resume_text)
    """

    def __init__(self) -> None:
        """Initialize ResumeParser service."""
        self._resume_agent = None
        self._file_processor = None
        logger.info("ResumeParser service initialized")

    def _get_resume_agent(self):
        """Lazy load ResumeAgent."""
        if self._resume_agent is None:
            from app.agents.resume_agent import ResumeAgent
            self._resume_agent = ResumeAgent()
        return self._resume_agent

    def _get_file_processor(self):
        """Lazy load FileProcessor."""
        if self._file_processor is None:
            from app.processors.file_processor import FileProcessor
            self._file_processor = FileProcessor()
        return self._file_processor

    def parse(
        self,
        resume_text: str,
        target_role: str = "General Technology Role",
    ) -> Dict[str, Any]:
        """
        Parse resume text and extract structured data.

        Args:
            resume_text: Raw resume text content
            target_role: Target job role for context

        Returns:
            dict: Parsed resume data
        """
        if not resume_text or not resume_text.strip():
            return {
                "success": False,
                "error": "No resume text provided.",
                "parsed_data": {},
            }

        try:
            agent = self._get_resume_agent()
            result = agent.run({
                "resume_text": resume_text,
                "target_role": target_role,
            })
            return result

        except Exception as exc:
            logger.error("Resume parsing failed: %s", str(exc))
            return {
                "success": False,
                "error": str(exc),
                "parsed_data": {},
            }

    def parse_file(
        self,
        file_path: str,
        target_role: str = "General Technology Role",
    ) -> Dict[str, Any]:
        """
        Parse resume from file path.

        Args:
            file_path: Path to resume file (PDF/DOCX)
            target_role: Target job role

        Returns:
            dict: Parsed resume data
        """
        try:
            processor = self._get_file_processor()
            resume_text = processor.extract_text(file_path)

            if not resume_text:
                return {
                    "success": False,
                    "error": "Could not extract text from file.",
                    "parsed_data": {},
                }

            return self.parse(
                resume_text=resume_text,
                target_role=target_role,
            )

        except Exception as exc:
            logger.error(
                "File parsing failed: %s | file: %s",
                str(exc),
                file_path,
            )
            return {
                "success": False,
                "error": str(exc),
                "parsed_data": {},
            }

    def extract_text_from_file(
        self,
        file_path: str,
    ) -> str:
        """
        Extract raw text from resume file.

        Args:
            file_path: Path to resume file

        Returns:
            str: Extracted text content
        """
        try:
            processor = self._get_file_processor()
            return processor.extract_text(file_path)
        except Exception as exc:
            logger.error(
                "Text extraction failed: %s", str(exc)
            )
            return ""