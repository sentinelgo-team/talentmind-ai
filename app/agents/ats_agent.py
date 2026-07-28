"""
TalentMind AI - ATS Analysis Agent
=====================================
Agent 02: Analyzes resume ATS compatibility,
scores keyword matching, format, and grammar.

Responsibilities:
    - ATS Score Generation
    - Keyword Analysis
    - Format Check
    - Grammar Analysis
    - Improvement Suggestions

Author  : TalentMind AI Team
Version : 1.0.0
"""

from __future__ import annotations

import logging
from typing import Any, Dict, Optional

from app.agents.base_agent import BaseAgent
from app.core.constants import AgentName, ScoreRange
from app.prompts.ats_prompts import ATS_ANALYSIS_PROMPT

logger = logging.getLogger(__name__)


class ATSAgent(BaseAgent):
    """
    Agent 02 - ATS Analysis Agent

    Analyzes resume for ATS compatibility and
    provides detailed scoring with suggestions.

    Input:
        resume_text : str  - Raw resume text
        parsed_resume: dict - Parsed resume data
        target_role : str  - Optional target job role

    Output:
        ats_score     : float  - Overall ATS score
        score_breakdown: dict  - Category scores
        suggestions   : list  - Improvement actions
        strengths     : list  - Resume strengths
        weaknesses    : list  - Resume weaknesses
    """

    def __init__(self) -> None:
        super().__init__(agent_name=AgentName.ATS)

    def run(
        self,
        input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Executes ATS analysis pipeline.

        Args:
            input_data: {
                resume_text  : str  (required)
                parsed_resume: dict (optional)
                target_role  : str  (optional)
            }

        Returns:
            dict: Complete ATS analysis result
        """
        self._log_start(list(input_data.keys()))

        resume_text   = input_data.get("resume_text", "")
        target_role   = input_data.get(
            "target_role", "General Technology Role"
        )

        if not resume_text:
            return {
                "success"   : False,
                "ats_score" : 0,
                "error"     : "No resume text provided.",
            }

        try:
            # Build and send prompt
            prompt = ATS_ANALYSIS_PROMPT.format(
                resume_text = resume_text[:8000],
                target_role = target_role,
            )

            self._logger.info(
                "Running ATS analysis | role=%s", target_role
            )

            response = self._call_llm(prompt)
            raw_data = self._parse_json_response(
                response_text=response,
                fallback={}
            )

            if not raw_data:
                return {
                    "success"   : False,
                    "ats_score" : 0,
                    "error"     : "Could not parse ATS response.",
                }

            # Extract and validate scores
            overall_score   = float(
                raw_data.get("overall_score", 0)
            )
            score_breakdown = raw_data.get(
                "score_breakdown", {}
            )

            # Determine score label
            score_label = self._get_score_label(overall_score)

            result = {
                "success"             : True,
                "ats_score"           : overall_score,
                "score_label"         : score_label,
                "score_breakdown"     : score_breakdown,
                "keyword_analysis"    : raw_data.get(
                    "keyword_analysis", {}
                ),
                "format_analysis"     : raw_data.get(
                    "format_analysis", {}
                ),
                "grammar_analysis"    : raw_data.get(
                    "grammar_analysis", {}
                ),
                "ats_suggestions"     : raw_data.get(
                    "ats_suggestions", []
                ),
                "strengths"           : raw_data.get(
                    "strengths", []
                ),
                "weaknesses"          : raw_data.get(
                    "weaknesses", []
                ),
                "improvement_priority": raw_data.get(
                    "improvement_priority", []
                ),
                "target_role"         : target_role,
                "error"               : None,
            }

            self._log_complete(["ats_score", "suggestions"])
            return result

        except Exception as exc:
            self._log_error(exc)
            return {
                "success"   : False,
                "ats_score" : 0,
                "error"     : str(exc),
            }

    def _get_score_label(self, score: float) -> str:
        """
        Returns human-readable label for score.

        Args:
            score: Numeric score 0-100

        Returns:
            str: Score label
        """
        if score >= ScoreRange.EXCELLENT_MIN:
            return "Excellent"
        elif score >= ScoreRange.GOOD_MIN:
            return "Good"
        elif score >= ScoreRange.AVERAGE_MIN:
            return "Average"
        else:
            return "Needs Improvement"