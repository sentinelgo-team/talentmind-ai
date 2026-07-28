"""
TalentMind AI - Risk Analysis Agent
=====================================
Agent 10: Assesses career risks, market risks,
and transition challenges for the candidate.

Responsibilities:
    - Career Risk Assessment
    - Skill Obsolescence Detection
    - Market Competition Analysis
    - Transition Risk Evaluation
    - Mitigation Planning

Author  : TalentMind AI Team
Version : 1.0.0
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List

from app.agents.base_agent import BaseAgent
from app.core.constants import AgentName, RiskLevel
from app.prompts.risk_prompts import RISK_ANALYSIS_PROMPT

logger = logging.getLogger(__name__)


class RiskAnalysisAgent(BaseAgent):
    """
    Agent 10 - Risk Analysis Agent

    Identifies and quantifies career risks with
    actionable mitigation strategies.

    Input:
        skill_analysis_result : dict
        skill_gap_result      : dict
        target_role           : str
        experience_level      : str
        experience_years      : float

    Output:
        overall_risk_level      : str
        overall_risk_score      : float
        risk_categories         : list
        career_stability_score  : float
        transition_risks        : list
        market_outlook          : dict
        mitigation_plan         : list
        summary                 : str
    """

    def __init__(self) -> None:
        super().__init__(agent_name=AgentName.RISK)

    def run(
        self,
        input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Executes risk analysis pipeline.

        Args:
            input_data: Candidate profile data

        Returns:
            dict: Risk assessment result
        """
        self._log_start(list(input_data.keys()))

        skill_result = input_data.get(
            "skill_analysis_result"
        ) or {}
        skill_gap_result = input_data.get(
            "skill_gap_result"
        ) or {}
        target_role = input_data.get(
            "target_role", "General Technology Role"
        )
        experience_level = input_data.get(
            "experience_level", "mid"
        )
        experience_years = input_data.get(
            "experience_years", 0
        )

        skills = self._extract_skills(skill_result)
        if not skills:
            return self._error_result(
                "No skill data available for risk analysis."
            )

        try:
            skill_gaps = [
                g.get("skill", "")
                for g in skill_gap_result.get(
                    "skill_gaps", []
                )[:5]
            ]
            primary_domain = skill_result.get(
                "primary_domain", "general_technology"
            )

            prompt = RISK_ANALYSIS_PROMPT.format(
                skills=", ".join(skills[:20]),
                experience_level=experience_level,
                target_role=target_role,
                primary_domain=primary_domain,
                experience_years=experience_years,
                skill_gaps=", ".join(skill_gaps),
            )

            self._logger.info(
                "Running risk analysis | role=%s",
                target_role
            )

            response = self._call_llm(prompt)
            raw_data = self._parse_json_response(
                response_text=response, fallback={}
            )

            if not raw_data:
                return self._error_result(
                    "Could not parse risk analysis response."
                )

            overall_score = float(
                raw_data.get("overall_risk_score", 50)
            )
            overall_score = max(0.0, min(100.0, overall_score))

            result = {
                "success": True,
                "error": None,
                "overall_risk_level": raw_data.get(
                    "overall_risk_level",
                    self._score_to_level(overall_score),
                ),
                "overall_risk_score": overall_score,
                "risk_categories": raw_data.get(
                    "risk_categories", []
                ),
                "career_stability_score": float(
                    raw_data.get("career_stability_score", 50)
                ),
                "transition_risks": raw_data.get(
                    "transition_risks", []
                ),
                "market_outlook": raw_data.get(
                    "market_outlook", {}
                ),
                "mitigation_plan": raw_data.get(
                    "mitigation_plan", []
                ),
                "summary": raw_data.get("summary", ""),
                "target_role": target_role,
                "experience_level": experience_level,
            }

            self._log_complete(
                ["overall_risk_level", "overall_risk_score"]
            )
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

    def _score_to_level(self, score: float) -> str:
        """Convert numeric score to risk level."""
        if score >= 81:
            return RiskLevel.CRITICAL
        elif score >= 61:
            return RiskLevel.HIGH
        elif score >= 31:
            return RiskLevel.MEDIUM
        else:
            return RiskLevel.LOW

    def _error_result(self, error_msg: str) -> Dict[str, Any]:
        """Return standardized error result."""
        return {
            "success": False,
            "error": error_msg,
            "overall_risk_level": RiskLevel.MEDIUM,
            "overall_risk_score": 0,
            "risk_categories": [],
            "career_stability_score": 0,
            "transition_risks": [],
            "market_outlook": {},
            "mitigation_plan": [],
            "summary": "",
            "target_role": "",
            "experience_level": "",
        }
