"""
TalentMind AI - Interview Preparation Agent
=============================================

Agent 06: Generates personalized interview questions based on resume analysis.

Author  : TalentMind AI Team
Version : 1.0.0
"""

from __future__ import annotations

import logging
from typing import Any, Dict

from app.agents.base_agent import BaseAgent
from app.core.constants import AgentName
from app.prompts.interview_prompts import INTERVIEW_QUESTIONS_PROMPT

logger = logging.getLogger(__name__)


class InterviewAgent(BaseAgent):
    """
    Agent 06 - Interview Preparation Agent

    Generates personalized interview questions including:
    - Technical Questions (10)
    - Coding Questions (10)
    - HR/Behavioral Questions (10)
    - Project-Based Questions (10)
    - Conceptual Questions (10)
    Total: 50 personalized interview questions

    Input:
        resume_text         : str
        parsed_resume       : dict
        target_role         : str
        experience_level    : str
        detected_skills     : list

    Output:
        technical_questions : list of dicts
        coding_questions    : list of dicts
        hr_questions        : list of dicts
        project_questions   : list of dicts
        conceptual_questions: list of dicts
        total_questions     : int
        difficulty_level    : str
        preparation_tips    : list
    """

    def __init__(self) -> None:
        super().__init__(agent_name=AgentName.INTERVIEW)

    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes interview question generation pipeline.

        Args:
            input_data: {
                resume_text         : str
                parsed_resume       : dict
                target_role         : str
                experience_level    : str
                detected_skills     : list
            }

        Returns:
            dict: Interview questions and preparation materials
        """
        self._log_start(list(input_data.keys()))

        resume_text = input_data.get("resume_text", "")
        parsed_resume = input_data.get("parsed_resume", {})
        target_role = input_data.get("target_role", "Software Developer")
        experience_level = input_data.get("experience_level", "Mid-level")
        detected_skills = input_data.get("detected_skills", [])

        if not resume_text:
            return {
                "success": False,
                "error": "No resume text provided.",
                "technical_questions": [],
                "coding_questions": [],
                "hr_questions": [],
                "project_questions": [],
                "conceptual_questions": [],
                "total_questions": 0,
                "difficulty_level": "",
                "preparation_tips": [],
            }

        try:
            # Extract skill list from parsed data if detected_skills is empty
            if not detected_skills and parsed_resume:
                detected_skills = parsed_resume.get("skills", [])

            prompt = INTERVIEW_QUESTIONS_PROMPT.format(
                resume_text=resume_text[:6000],
                target_role=target_role,
                experience_level=experience_level,
                detected_skills=", ".join(detected_skills[:20]) if detected_skills else "Not specified",
            )

            self._logger.info(
                "Generating interview questions | role=%s | experience=%s",
                target_role,
                experience_level,
            )

            response = self._call_llm(prompt)
            raw_data = self._parse_json_response(
                response_text=response,
                fallback={}
            )

            if not raw_data:
                return {
                    "success": False,
                    "error": "Could not parse interview questions.",
                    "technical_questions": [],
                    "coding_questions": [],
                    "hr_questions": [],
                    "project_questions": [],
                    "conceptual_questions": [],
                    "total_questions": 0,
                    "difficulty_level": "",
                    "preparation_tips": [],
                }

            result = {
                "success": True,
                "technical_questions": raw_data.get("technical_questions", []),
                "coding_questions": raw_data.get("coding_questions", []),
                "hr_questions": raw_data.get("hr_questions", []),
                "project_questions": raw_data.get("project_questions", []),
                "conceptual_questions": raw_data.get("conceptual_questions", []),
                "total_questions": raw_data.get("total_questions", 0),
                "difficulty_level": raw_data.get("difficulty_level", "medium"),
                "preparation_tips": raw_data.get("preparation_tips", []),
                "error": None,
            }

            self._log_complete([
                "technical_questions",
                "coding_questions",
                "hr_questions",
                "project_questions",
                "conceptual_questions"
            ])
            return result

        except Exception as exc:
            self._log_error(exc)
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