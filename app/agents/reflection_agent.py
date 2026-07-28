"""
TalentMind AI - Reflection Agent
==================================
Agent 09: Quality assurance agent that reviews all
other agent outputs for consistency and completeness.

Responsibilities:
    - Cross-agent Consistency Check
    - Completeness Assessment
    - Confidence Rating
    - Quality Flags
    - User Recommendations

Author  : TalentMind AI Team
Version : 1.0.0
"""

from __future__ import annotations

import logging
from typing import Any, Dict

from app.agents.base_agent import BaseAgent
from app.core.constants import AgentName
from app.prompts.reflection_prompts import REFLECTION_PROMPT

logger = logging.getLogger(__name__)


class ReflectionAgent(BaseAgent):
    """
    Agent 09 - Reflection & Quality Agent

    Reviews all agent outputs for internal consistency,
    identifies contradictions, and rates overall quality.

    Input:
        resume_result     : dict
        ats_result        : dict
        skill_result      : dict
        skill_gap_result  : dict
        job_matching_result: dict
        target_role       : str
        experience_level  : str

    Output:
        consistency_score        : float
        consistency_issues       : list
        completeness_assessment  : dict
        confidence_levels        : dict
        recommendations_for_user : list
        quality_flags            : list
        overall_quality          : dict
    """

    def __init__(self) -> None:
        super().__init__(agent_name=AgentName.REFLECTION)

    def run(
        self,
        input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Executes reflection and quality assessment.

        Args:
            input_data: All agent results to review

        Returns:
            dict: Quality assessment result
        """
        self._log_start(list(input_data.keys()))

        resume_result = input_data.get("resume_result") or {}
        ats_result = input_data.get("ats_result") or {}
        skill_result = input_data.get("skill_result") or {}
        skill_gap_result = input_data.get(
            "skill_gap_result"
        ) or {}
        job_matching_result = input_data.get(
            "job_matching_result"
        ) or {}
        target_role = input_data.get(
            "target_role", "General Technology Role"
        )
        experience_level = input_data.get(
            "experience_level", "mid"
        )

        agent_count = sum(
            1 for r in [
                resume_result, ats_result, skill_result,
                skill_gap_result, job_matching_result
            ] if r.get("success")
        )

        if agent_count == 0:
            return self._error_result(
                "No successful agent results to review."
            )

        try:
            prompt = REFLECTION_PROMPT.format(
                resume_result=self._summarize(
                    resume_result, 300
                ),
                ats_score=ats_result.get("ats_score", "N/A"),
                skill_result=self._summarize(
                    skill_result, 300
                ),
                skill_gap_result=self._summarize(
                    skill_gap_result, 300
                ),
                job_matching_result=self._summarize(
                    job_matching_result, 300
                ),
                target_role=target_role,
                experience_level=experience_level,
            )

            self._logger.info(
                "Running reflection analysis | agents_reviewed=%d",
                agent_count
            )

            response = self._call_llm(prompt)
            raw_data = self._parse_json_response(
                response_text=response, fallback={}
            )

            if not raw_data:
                return self._error_result(
                    "Could not parse reflection response."
                )

            result = {
                "success": True,
                "error": None,
                "consistency_score": float(
                    raw_data.get("consistency_score", 0)
                ),
                "consistency_issues": raw_data.get(
                    "consistency_issues", []
                ),
                "completeness_assessment": raw_data.get(
                    "completeness_assessment", {}
                ),
                "confidence_levels": raw_data.get(
                    "confidence_levels", {}
                ),
                "recommendations_for_user": raw_data.get(
                    "recommendations_for_user", []
                ),
                "quality_flags": raw_data.get(
                    "quality_flags", []
                ),
                "overall_quality": raw_data.get(
                    "overall_quality", {}
                ),
                "agents_reviewed": agent_count,
            }

            self._log_complete(
                ["consistency_score", "overall_quality"]
            )
            return result

        except Exception as exc:
            self._log_error(exc)
            return self._error_result(str(exc))

    def _summarize(
        self, data: Dict[str, Any], max_chars: int
    ) -> str:
        """Create a compact summary of agent result for the prompt."""
        import json
        keys_to_keep = [
            "success", "error", "ats_score", "score_label",
            "overall_readiness_score", "readiness_label",
            "top_skills", "skill_gaps", "career_paths",
            "matched_skills", "critical_gaps_count",
            "candidate_name", "skills_count",
        ]
        filtered = {
            k: v for k, v in data.items()
            if k in keys_to_keep and v
        }
        text = json.dumps(filtered, default=str)
        if len(text) > max_chars:
            text = text[:max_chars] + "..."
        return text

    def _error_result(self, error_msg: str) -> Dict[str, Any]:
        """Return standardized error result."""
        return {
            "success": False,
            "error": error_msg,
            "consistency_score": 0,
            "consistency_issues": [],
            "completeness_assessment": {},
            "confidence_levels": {},
            "recommendations_for_user": [],
            "quality_flags": [],
            "overall_quality": {},
            "agents_reviewed": 0,
        }
