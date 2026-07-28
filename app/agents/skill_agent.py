"""
TalentMind AI - Skill Analysis Agent
=======================================
Agent 03: Detects, classifies, and scores
all skills found in the resume.

Author  : TalentMind AI Team
Version : 1.0.0
"""

from __future__ import annotations

import logging
from typing import Any, Dict

from app.agents.base_agent import BaseAgent
from app.core.constants import AgentName
from app.prompts.skill_prompts import SKILL_ANALYSIS_PROMPT

logger = logging.getLogger(__name__)


class SkillAnalysisAgent(BaseAgent):
    """
    Agent 03 - Skill Analysis Agent

    Input:
        resume_text   : str
        parsed_resume : dict
        target_role   : str

    Output:
        detected_skills    : list
        skill_categories   : dict
        proficiency_summary: dict
        industry_comparison: dict
        skill_scores       : dict
        top_skills         : list
        skill_gaps         : list
        recommendations    : list
    """

    def __init__(self) -> None:
        super().__init__(agent_name=AgentName.SKILL)

    def run(
        self,
        input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Executes skill analysis pipeline.

        Args:
            input_data: {
                resume_text  : str
                parsed_resume: dict
                target_role  : str
            }

        Returns:
            dict: Complete skill analysis
        """
        self._log_start(list(input_data.keys()))

        resume_text = input_data.get("resume_text", "")
        target_role = input_data.get(
            "target_role", "Software Developer"
        )

        if not resume_text:
            return {
                "success": False,
                "error"  : "No resume text provided.",
            }

        try:
            prompt = SKILL_ANALYSIS_PROMPT.format(
                resume_text = resume_text[:8000],
                target_role = target_role,
            )

            self._logger.info(
                "Running skill analysis | role=%s",
                target_role
            )

            response = self._call_llm(prompt)
            raw_data = self._parse_json_response(
                response_text=response,
                fallback={}
            )

            if not raw_data:
                return {
                    "success": False,
                    "error"  : "Could not parse skill data.",
                }

            result = {
                "success"           : True,
                "detected_skills"   : raw_data.get(
                    "detected_skills", []
                ),
                "skill_categories"  : raw_data.get(
                    "skill_categories", {}
                ),
                "proficiency_summary": raw_data.get(
                    "proficiency_summary", {}
                ),
                "industry_comparison": raw_data.get(
                    "industry_comparison", {}
                ),
                "skill_scores"      : raw_data.get(
                    "skill_scores", {}
                ),
                "top_skills"        : raw_data.get(
                    "top_skills", []
                ),
                "skill_gaps"        : raw_data.get(
                    "skill_gaps", []
                ),
                "recommendations"   : raw_data.get(
                    "recommendations", []
                ),
                "total_skills_count": raw_data.get(
                    "total_skills_count", 0
                ),
                "target_role"       : target_role,
                "error"             : None,
            }

            self._log_complete(["detected_skills","skill_scores"])
            return result

        except Exception as exc:
            self._log_error(exc)
            return {
                "success": False,
                "error"  : str(exc),
            }