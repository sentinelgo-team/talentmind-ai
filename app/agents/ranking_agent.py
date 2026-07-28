"""
TalentMind AI - Ranking Agent
================================
Agent 08: Evaluates and ranks candidate profiles
across multiple dimensions.

Responsibilities:
    - Multi-dimensional Scoring
    - Competitive Positioning
    - Hiring Recommendations
    - Improvement Impact Analysis

Author  : TalentMind AI Team
Version : 1.0.0
"""

from __future__ import annotations

import logging
from typing import Any, Dict

from app.agents.base_agent import BaseAgent
from app.core.constants import AgentName
from app.prompts.ranking_prompts import RANKING_PROMPT

logger = logging.getLogger(__name__)


class RankingAgent(BaseAgent):
    """
    Agent 08 - Candidate Ranking Agent

    Evaluates candidate across multiple dimensions
    and provides competitive positioning.

    Input:
        resume_text           : str
        target_role           : str
        experience_level      : str
        skill_analysis_result : dict
        ats_result            : dict
        skill_gap_result      : dict

    Output:
        overall_rank_score    : float
        rank_label            : str
        dimension_scores      : dict
        competitive_position  : dict
        hiring_recommendation : dict
        improvement_impact    : list
    """

    def __init__(self) -> None:
        super().__init__(agent_name=AgentName.RANKING)

    def run(
        self,
        input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Executes ranking assessment pipeline.

        Args:
            input_data: Combined candidate data

        Returns:
            dict: Ranking assessment result
        """
        self._log_start(list(input_data.keys()))

        resume_text = input_data.get("resume_text", "")
        target_role = input_data.get(
            "target_role", "General Technology Role"
        )
        experience_level = input_data.get(
            "experience_level", "mid"
        )
        skill_result = input_data.get(
            "skill_analysis_result"
        ) or {}
        ats_result = input_data.get("ats_result") or {}
        skill_gap_result = input_data.get(
            "skill_gap_result"
        ) or {}

        if not resume_text:
            return self._error_result(
                "No resume text provided."
            )

        try:
            skills_count = len(
                skill_result.get("top_skills", [])
            )
            ats_score = ats_result.get("ats_score", 0)
            skill_match_pct = skill_gap_result.get(
                "overall_readiness_score", 0
            )
            critical_gaps = skill_gap_result.get(
                "critical_gaps_count", 0
            )
            strengths = ", ".join(
                skill_gap_result.get("strengths", [])[:5]
            )

            prompt = RANKING_PROMPT.format(
                resume_text=resume_text[:4000],
                target_role=target_role,
                experience_level=experience_level,
                skills_count=skills_count,
                ats_score=ats_score,
                skill_match_pct=skill_match_pct,
                critical_gaps=critical_gaps,
                strengths=strengths or "Not yet analyzed",
            )

            self._logger.info(
                "Running ranking assessment | role=%s",
                target_role
            )

            response = self._call_llm(prompt)
            raw_data = self._parse_json_response(
                response_text=response, fallback={}
            )

            if not raw_data:
                return self._error_result(
                    "Could not parse ranking response."
                )

            result = {
                "success": True,
                "error": None,
                "overall_rank_score": float(
                    raw_data.get("overall_rank_score", 0)
                ),
                "rank_label": raw_data.get(
                    "rank_label", "Unranked"
                ),
                "dimension_scores": raw_data.get(
                    "dimension_scores", {}
                ),
                "competitive_position": raw_data.get(
                    "competitive_position", {}
                ),
                "hiring_recommendation": raw_data.get(
                    "hiring_recommendation", {}
                ),
                "improvement_impact": raw_data.get(
                    "improvement_impact", []
                ),
                "target_role": target_role,
            }

            self._log_complete(
                ["overall_rank_score", "rank_label"]
            )
            return result

        except Exception as exc:
            self._log_error(exc)
            return self._error_result(str(exc))

    def _error_result(self, error_msg: str) -> Dict[str, Any]:
        """Return standardized error result."""
        return {
            "success": False,
            "error": error_msg,
            "overall_rank_score": 0,
            "rank_label": "Unranked",
            "dimension_scores": {},
            "competitive_position": {},
            "hiring_recommendation": {},
            "improvement_impact": [],
            "target_role": "",
        }
