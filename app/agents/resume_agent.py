"""
TalentMind AI - Resume Agent
==============================
Agent 01: Parses and extracts structured information
from raw resume text using Google Gemini AI.

Responsibilities:
    - Resume parsing
    - Information extraction
    - Education analysis
    - Skills analysis
    - Project analysis
    - Experience analysis

Author  : TalentMind AI Team
Version : 1.0.0
"""

from __future__ import annotations

import logging
from typing import Any, Dict

from app.agents.base_agent import BaseAgent
from app.core.constants import AgentName
from app.core.exceptions import AgentError
from app.models.resume import ParsedResume
from app.prompts.resume_prompts import RESUME_PARSING_PROMPT

logger = logging.getLogger(__name__)


class ResumeAgent(BaseAgent):
    """
    Agent 01 - Resume Parsing Agent

    Uses Gemini AI to extract structured data from
    raw resume text. Outputs a validated ParsedResume
    Pydantic model for downstream agents.

    Input:
        resume_text : str  - Raw extracted resume text
        resume_id   : str  - Resume UUID for tracking

    Output:
        parsed_resume : dict  - Structured resume data
        success       : bool
        error         : str or None
    """

    def __init__(self) -> None:
        super().__init__(agent_name=AgentName.RESUME)

    def run(
        self,
        input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Executes resume parsing pipeline.

        Args:
            input_data: {
                resume_text : str  (required)
                resume_id   : str  (optional)
            }

        Returns:
            dict: {
                success       : bool
                parsed_resume : dict
                candidate_name: str
                skills_count  : int
                error         : str or None
            }
        """
        self._log_start(list(input_data.keys()))

        resume_text = input_data.get("resume_text", "")
        resume_id   = input_data.get("resume_id", "unknown")

        if not resume_text or len(resume_text.strip()) < 50:
            return {
                "success"       : False,
                "parsed_resume" : {},
                "error"         : "Resume text is too short.",
            }

        try:
            # Step 1 — Build prompt
            prompt = RESUME_PARSING_PROMPT.format(
                resume_text=resume_text[:8000]
            )

            # Step 2 — Call Gemini
            self._logger.info(
                "Calling Gemini | resume_id=%s", resume_id
            )
            response = self._call_llm(prompt)

            # Step 3 — Parse JSON response
            raw_data = self._parse_json_response(
                response_text=response,
                fallback={}
            )

            if not raw_data:
                return {
                    "success"       : False,
                    "parsed_resume" : {},
                    "error"         : "Could not parse resume data.",
                }

            # Step 4 — Validate with Pydantic
            parsed = self._validate_and_build(raw_data)

            # Step 5 — Build result
            result = {
                "success"        : True,
                "parsed_resume"  : parsed.model_dump(),
                "candidate_name" : parsed.contact_info.name,
                "skills_count"   : len(parsed.skills),
                "education_count": len(parsed.education),
                "experience_count": len(parsed.experience),
                "projects_count" : len(parsed.projects),
                "error"          : None,
            }

            self._log_complete(list(result.keys()))
            return result

        except Exception as exc:
            self._log_error(exc)
            return {
                "success"       : False,
                "parsed_resume" : {},
                "error"         : str(exc),
            }

    def _validate_and_build(
        self,
        raw_data: dict
    ) -> ParsedResume:
        """
        Validates raw dict and builds ParsedResume model.
        Handles missing or malformed fields gracefully.

        Args:
            raw_data: Raw parsed JSON from Gemini

        Returns:
            ParsedResume: Validated Pydantic model
        """
        try:
            return ParsedResume(**raw_data)

        except Exception as exc:
            self._logger.warning(
                "Pydantic validation warning | error=%s | "
                "attempting partial build", exc
            )
            # Build with available fields
            return ParsedResume(
                contact_info=raw_data.get("contact_info", {}),
                summary=raw_data.get("summary"),
                education=raw_data.get("education", []),
                experience=raw_data.get("experience", []),
                projects=raw_data.get("projects", []),
                certifications=raw_data.get("certifications", []),
                skills=raw_data.get("skills", []),
                languages=raw_data.get("languages", []),
                total_experience_years=raw_data.get(
                    "total_experience_years", 0.0
                ),
            )
            