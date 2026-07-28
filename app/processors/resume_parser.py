"""
Resume Parser Module for TalentMind AI
======================================
Handles resume parsing by combining file processing and agent-based analysis.

This module provides a unified interface for extracting text from resume files
(PDF, DOCX, TXT) and parsing them into structured data using the ResumeAgent.

Typical usage:
    from app.processors.resume_parser import ResumeParser
    parser = ResumeParser()
    result = parser.parse_file("path/to/resume.pdf")
"""

from __future__ import annotations

import logging
from typing import Any, Dict

from app.agents.resume_agent import ResumeAgent
from app.processors.file_processor import FileProcessor

logger = logging.getLogger(__name__)


class ResumeParser:
    """
    Unified resume parser that combines file processing and AI-based analysis.
    
    Responsibilities:
        - Process resume files (PDF, DOCX, TXT) to extract raw text
        - Use ResumeAgent to extract structured data from the text
        - Provide a simple interface for resume parsing operations
        
    Why needed:
        Combines low-level file handling with high-level AI analysis into
        a single, easy-to-use component for resume processing workflows.
    """
    
    def __init__(self) -> None:
        """Initialize the resume parser with required dependencies."""
        self._file_processor = FileProcessor()
        self._resume_agent = ResumeAgent()
        logger.info("ResumeParser initialized")
    
    def parse_file(
        self, 
        file_path: str,
        target_role: str = "General Technology Role"
    ) -> Dict[str, Any]:
        """
        Parse a resume file and extract structured data.
        
        Args:
            file_path: Path to the resume file (PDF, DOCX, or TXT)
            target_role: Target job role for context-aware analysis
            
        Returns:
            Dictionary containing:
                - success: Boolean indicating if parsing succeeded
                - parsed_data: Structured resume data (if successful)
                - error: Error message (if unsuccessful)
                - file_info: Metadata about the processed file
        """
        logger.info(f"Parsing resume file: {file_path}")
        
        try:
            # Step 1: Extract text from file using FileProcessor
            extraction_result = self._file_processor.process_file(file_path)
            
            if not extraction_result["success"]:
                return {
                    "success": False,
                    "error": extraction_result["error"],
                    "parsed_data": {},
                    "file_info": {}
                }
                
            raw_text = extraction_result["text"]
            file_info = extraction_result["file_info"]
            
            # Step 2: Parse text using ResumeAgent
            parse_result = self._resume_agent.parse_resume(
                resume_text=raw_text,
                target_role=target_role
            )
            
            if not parse_result["success"]:
                return {
                    "success": False,
                    "error": parse_result["error"],
                    "parsed_data": {},
                    "file_info": file_info
                }
                
            logger.info(f"Successfully parsed resume: {file_path}")
            return {
                "success": True,
                "parsed_data": parse_result["parsed_data"],
                "error": None,
                "file_info": file_info
            }
            
        except Exception as exc:
            logger.error(f"Failed to parse resume {file_path}: {exc}", exc_info=True)
            return {
                "success": False,
                "error": str(exc),
                "parsed_data": {},
                "file_info": {}
            }
    
    def parse_text(
        self,
        resume_text: str,
        target_role: str = "General Technology Role"
    ) -> Dict[str, Any]:
        """
        Parse raw resume text and extract structured data.
        
        Args:
            resume_text: Raw text content of the resume
            target_role: Target job role for context-aware analysis
            
        Returns:
            Dictionary containing:
                - success: Boolean indicating if parsing succeeded
                - parsed_data: Structured resume data (if successful)
                - error: Error message (if unsuccessful)
        """
        if not resume_text or not resume_text.strip():
            return {
                "success": False,
                "error": "No resume text provided",
                "parsed_data": {}
            }
            
        try:
            result = self._resume_agent.parse_resume(
                resume_text=resume_text,
                target_role=target_role
            )
            
            if not result["success"]:
                return {
                    "success": False,
                    "error": result["error"],
                    "parsed_data": {}
                }
                
            return {
                "success": True,
                "parsed_data": result["parsed_data"],
                "error": None
            }
            
        except Exception as exc:
            logger.error(f"Failed to parse resume text: {exc}", exc_info=True)
            return {
                "success": False,
                "error": str(exc),
                "parsed_data": {}
            }


# Convenience function for quick parsing
def parse_resume_file(file_path: str, target_role: str = "General Technology Role") -> Dict[str, Any]:
    """
    Convenience function to parse a resume file without instantiating the class.
    
    Args:
        file_path: Path to the resume file
        target_role: Target job role for context-aware analysis
        
    Returns:
        Dictionary with parsing results (see ResumeParser.parse_file)
    """
    parser = ResumeParser()
    return parser.parse_file(file_path, target_role)