"""
TalentMind AI - ATS Analyzer Service
========================================
Purpose: Service layer for ATS analysis operations.
         Bridges UI pages with ATSAgent.

Author  : TalentMind AI Team
Version : 1.0.0
"""

from __future__ import annotations

import logging
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


class ATSAnalyzer:
    """
    Service class for ATS analysis operations.

    Usage:
        analyzer = ATSAnalyzer()
        result = analyzer.analyze(resume_text, target_role)
    """

    def __init__(self) -> None:
        """Initialize ATSAnalyzer service."""
        self._ats_agent = None
        logger.info("ATSAnalyzer service initialized")

    def _get_ats_agent(self):
        """Lazy load ATSAgent."""
        if self._ats_agent is None:
            from app.agents.ats_agent import ATSAgent
            self._ats_agent = ATSAgent()
        return self._ats_agent

    def analyze(
        self,
        resume_text: str,
        target_role: str = "General Technology Role",
        parsed_resume: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Run ATS analysis on resume.

        Args:
            resume_text: Raw resume text
            target_role: Target job role
            parsed_resume: Optional pre-parsed data

        Returns:
            dict: ATS analysis result
        """
        if not resume_text or not resume_text.strip():
            return {
                "success": False,
                "error": "No resume text provided.",
                "ats_score": 0,
            }

        try:
            agent = self._get_ats_agent()
            return agent.run({
                "resume_text": resume_text,
                "target_role": target_role,
                "parsed_resume": parsed_resume or {},
            })

        except Exception as exc:
            logger.error("ATS analysis failed: %s", str(exc))
            return {
                "success": False,
                "error": str(exc),
                "ats_score": 0,
            }