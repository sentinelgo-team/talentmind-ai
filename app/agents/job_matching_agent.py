"""
TalentMind AI - Job Matching Agent
==================================

Agent 04: Matches candidate to suitable job roles based on resume analysis.

Author  : TalentMind AI Team
Version : 1.0.0
"""

from __future__ import annotations

import logging
from typing import Any, Dict

from app.agents.base_agent import BaseAgent
from app.core.constants import AgentName
from app.prompts.job_matching_prompts import JOB_MATCHING_PROMPT

logger = logging.getLogger(__name__)


class JobMatchingAgent(BaseAgent):
    """
    Agent 04 - Job Matching Agent

    Matches candidate to top 5 job roles, suggests career paths, recommends internships (for freshers),
    analyzes industry fit, and provides salary expectations.

    Input:
        resume_text      : str
        detected_skills  : list
        experience_level : str
        primary_domain   : str
        target_role      : str (optional preference)

    Output:
        job_matches      : list (top 5 job matches)
        career_paths     : list
        internship_recs  : list (if fresher)
        industry_fit     : list
        salary_range     : dict
        next_role_suggestion: str
        total_matches    : int
    """

    def __init__(self) -> None:
        super().__init__(agent_name=AgentName.JOB_MATCHING)

    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes job matching pipeline.

        Args:
            input_data: {
                resume_text       : str
                detected_skills   : list
                experience_level  : str
                primary_domain    : str
                target_role       : str (optional)
            }

        Returns:
            dict: Job matching results and recommendations
        """
        self._log_start(list(input_data.keys()))

        resume_text = input_data.get("resume_text", "")
        detected_skills = input_data.get("detected_skills", [])
        experience_level = input_data.get("experience_level", "Mid-level")
        primary_domain = input_data.get("primary_domain", "Software Development")
        target_role = input_data.get("target_role", "")

        if not resume_text:
            return {
                "success": False,
                "error": "No resume text provided.",
                "job_matches": [],
                "career_paths": [],
                "internship_recs": [],
                "industry_fit": [],
                "salary_range": {},
                "next_role_suggestion": "",
                "total_matches": 0,
            }

        try:
            prompt = JOB_MATCHING_PROMPT.substitute(
                resume_text=resume_text[:8000],
                detected_skills=", ".join(detected_skills) if detected_skills else "Not specified",
                experience_level=experience_level,
                primary_domain=primary_domain,
                target_role=target_role if target_role else "Not specified (open to opportunities)",
            )

            self._logger.info(
                "Running job matching | experience=%s | domain=%s",
                experience_level,
                primary_domain,
            )

            response = self._call_llm(prompt)
            raw_data = self._parse_json_response(
                response_text=response,
                fallback={}
            )

            if not raw_data or not isinstance(raw_data, dict):
                return {
                    "success": False,
                    "error": "Could not parse job matching results.",
                    "job_matches": [],
                    "career_paths": [],
                    "internship_recs": [],
                    "industry_fit": [],
                    "salary_range": {},
                    "next_role_suggestion": "",
                    "total_matches": 0,
                }

            # Ensure the result has the expected structure
            result = {
                "success": True,
                "job_matches": raw_data.get("job_matches", []),
                "career_paths": raw_data.get("career_paths", []),
                "internship_recs": raw_data.get("internship_recs", []),
                "industry_fit": raw_data.get("industry_fit", []),
                "salary_range": raw_data.get("salary_range", {}),
                "next_role_suggestion": raw_data.get("next_role_suggestion", ""),
                "total_matches": raw_data.get("total_matches", 0),
                "error": None,
            }

            self._log_complete(["job_matches", "career_paths", "salary_range"])
            return result

        except Exception as exc:
            self._log_error(exc)
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