"""
TalentMind AI - Job Matching Service
====================================

Service layer for Job Matching Agent.

Author  : TalentMind AI Team
Version : 1.0.0
"""

from __future__ import annotations

import logging
from typing import Any, Dict

from app.agents.job_matching_agent import JobMatchingAgent
from app.core.constants import AgentName

logger = logging.getLogger(__name__)


class JobMatchingService:
    """
    Service for job matching and career recommendations.
    """

    def __init__(self) -> None:
        self.agent = JobMatchingAgent()
        self._logger = logging.getLogger(f"services.{AgentName.JOB_MATCHING}")

    def match_jobs(
        self,
        resume_text: str,
        detected_skills: list,
        experience_level: str,
        primary_domain: str,
        target_role: str = ""
    ) -> Dict[str, Any]:
        """
        Match candidate to job roles and provide career recommendations.

        Args:
            resume_text: Raw resume text
            detected_skills: List of skills detected from resume
            experience_level: Candidate's experience level
            primary_domain: Primary domain/industry of candidate
            target_role: Optional target role preference

        Returns:
            Dictionary containing job matches and career recommendations
        """
        self._logger.info(
            "Matching jobs | experience=%s | domain=%s",
            experience_level,
            primary_domain,
        )

        input_data = {
            "resume_text": resume_text,
            "detected_skills": detected_skills,
            "experience_level": experience_level,
            "primary_domain": primary_domain,
            "target_role": target_role,
        }

        try:
            result = self.agent.run(input_data)
            self._logger.info(
                "Job matching completed | success=%s | matches=%d",
                result.get("success", False),
                result.get("total_matches", 0),
            )
            return result
        except Exception as exc:
            self._logger.error("Job matching failed | error=%s", exc)
            return {
                "success": False,
                "error": str(exc),
                "job_matches": [],
                "career_paths": [],
                "internship_recs": [],
                "industry_fit": [],
                "salary_range": {},
                "next_role_suggestion": "",
                "total_matches": 0,
            }