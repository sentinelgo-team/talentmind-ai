"""
TalentMind AI - Recommendation Agent
======================================
Agent 07: Generates personalized career recommendations
based on complete candidate profile analysis.

Responsibilities:
    - Career Path Recommendations
    - Immediate Action Items
    - Skill Development Planning
    - Networking Suggestions
    - Resume Improvement Tips
    - Market Insights

Author  : TalentMind AI Team
Version : 1.0.0
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List

from app.agents.base_agent import BaseAgent
from app.core.constants import AgentName
from app.prompts.recommendation_prompts import RECOMMENDATION_PROMPT

logger = logging.getLogger(__name__)


class RecommendationAgent(BaseAgent):
    """
    Agent 07 - Career Recommendation Agent

    Synthesizes all analysis results to generate
    actionable career recommendations.

    Input:
        skill_analysis_result : dict
        skill_gap_result      : dict
        ats_result            : dict
        target_role           : str
        experience_level      : str

    Output:
        career_paths           : list
        immediate_actions      : list
        skill_development_plan : list
        networking_suggestions : list
        resume_improvements    : list
        market_insights        : dict
        overall_readiness      : dict
    """

    def __init__(self) -> None:
        super().__init__(agent_name=AgentName.RECOMMENDATION)

    def run(
        self,
        input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Executes recommendation generation pipeline.

        Args:
            input_data: Combined analysis results

        Returns:
            dict: Personalized recommendations
        """
        self._log_start(list(input_data.keys()))

        skill_result = input_data.get("skill_analysis_result") or {}
        skill_gap_result = input_data.get("skill_gap_result") or {}
        ats_result = input_data.get("ats_result") or {}
        target_role = input_data.get(
            "target_role", "General Technology Role"
        )
        experience_level = input_data.get(
            "experience_level", "mid"
        )

        skills = self._extract_skills(skill_result)
        if not skills:
            return self._error_result(
                "No skill data available for recommendations."
            )

        try:
            skill_gaps = [
                g.get("skill", "")
                for g in skill_gap_result.get("skill_gaps", [])[:5]
            ]
            ats_score = ats_result.get("ats_score", 0)
            primary_domain = skill_result.get(
                "primary_domain", "general_technology"
            )

            prompt = RECOMMENDATION_PROMPT.format(
                skills=", ".join(skills[:20]),
                experience_level=experience_level,
                target_role=target_role,
                primary_domain=primary_domain,
                ats_score=ats_score,
                skill_gaps=", ".join(skill_gaps),
            )

            self._logger.info(
                "Generating recommendations | role=%s",
                target_role
            )

            response = self._call_llm(prompt)
            raw_data = self._parse_json_response(
                response_text=response, fallback={}
            )

            if not raw_data:
                return self._error_result(
                    "Could not parse recommendation response."
                )

            result = {
                "success": True,
                "error": None,
                "career_paths": raw_data.get("career_paths", []),
                "immediate_actions": raw_data.get(
                    "immediate_actions", []
                ),
                "skill_development_plan": raw_data.get(
                    "skill_development_plan", []
                ),
                "networking_suggestions": raw_data.get(
                    "networking_suggestions", []
                ),
                "resume_improvements": raw_data.get(
                    "resume_improvements", []
                ),
                "market_insights": raw_data.get(
                    "market_insights", {}
                ),
                "overall_readiness": raw_data.get(
                    "overall_readiness", {}
                ),
                "target_role": target_role,
                "experience_level": experience_level,
            }

            self._log_complete(list(result.keys()))
            return result

        except Exception as exc:
            self._log_error(exc)
            return self._error_result(str(exc))

    def _extract_skills(
        self, skill_result: Dict[str, Any]
    ) -> List[str]:
        """Extract skill names from skill analysis result."""
        skills: List[str] = []

        top_skills = skill_result.get("top_skills", [])
        if isinstance(top_skills, list):
            for s in top_skills:
                if isinstance(s, str):
                    skills.append(s)
                elif isinstance(s, dict):
                    skills.append(s.get("skill", ""))

        tech_skills = skill_result.get("technical_skills", [])
        for s in tech_skills:
            if isinstance(s, dict):
                skills.append(s.get("skill", ""))
            elif isinstance(s, str):
                skills.append(s)

        return [s for s in skills if s]

    def _error_result(self, error_msg: str) -> Dict[str, Any]:
        """Return standardized error result."""
        return {
            "success": False,
            "error": error_msg,
            "career_paths": [],
            "immediate_actions": [],
            "skill_development_plan": [],
            "networking_suggestions": [],
            "resume_improvements": [],
            "market_insights": {},
            "overall_readiness": {},
            "target_role": "",
            "experience_level": "",
        }
