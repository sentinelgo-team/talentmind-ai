"""
TalentMind AI - Interview Service
=================================

Service layer for Interview Preparation Agent.

Author  : TalentMind AI Team
Version : 1.0.0
"""

from __future__ import annotations

import logging
from typing import Any, Dict

from app.agents.interview_agent import InterviewAgent
from app.core.constants import AgentName

logger = logging.getLogger(__name__)


class InterviewService:
    """
    Service for generating interview questions based on resume analysis.

    This service orchestrates the InterviewAgent to generate personalized
    interview questions for candidates.
    """

    def __init__(self) -> None:
        self.agent = InterviewAgent()
        self._logger = logging.getLogger(f"services.{AgentName.INTERVIEW}")

    def generate_interview_questions(
        self,
        resume_text: str,
        parsed_resume: dict,
        target_role: str,
        experience_level: str,
        detected_skills: list
    ) -> Dict[str, Any]:
        """
        Generate personalized interview questions for a candidate.

        Args:
            resume_text: Raw resume text
            parsed_resume: Parsed resume data from resume parser
            target_role: Target job role for the interview
            experience_level: Candidate's experience level (Entry, Mid, Senior)
            detected_skills: List of skills detected from resume analysis

        Returns:
            Dictionary containing interview questions and preparation materials
        """
        self._logger.info(
            "Generating interview questions | role=%s | experience=%s",
            target_role,
            experience_level,
        )

        input_data = {
            "resume_text": resume_text,
            "parsed_resume": parsed_resume,
            "target_role": target_role,
            "experience_level": experience_level,
            "detected_skills": detected_skills,
        }

        try:
            result = self.agent.run(input_data)
            self._logger.info(
                "Interview questions generated | success=%s | questions=%d",
                result.get("success", False),
                result.get("total_questions", 0),
            )
            return result
        except Exception as exc:
            self._logger.error(
                "Failed to generate interview questions | error=%s", exc
            )
            return {
                "success": False,
                "error": str(exc),
                "technical_questions": [],
                "coding_questions": [],
                "hr_questions": [],
                "project_questions": [],
                "conceptual_questions": [],
                "total_questions": 0,
                "difficulty_level": "",
                "preparation_tips": [],
            }