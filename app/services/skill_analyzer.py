"""
TalentMind AI - Skill Analyzer Service
========================================
Purpose: Service layer that orchestrates SkillAnalysisAgent
         and SkillGapAgent for the UI pages.

Provides all methods that UI pages need:
    - analyze()
    - analyze_skill_gap()
    - analyze_skills_only()
    - analyze_gaps_only()
    - get_supported_roles()
    - get_experience_levels()
    - parse_experience_level()

Architecture:
    UI Page
       │
       ▼
    SkillAnalyzer (this service)
       │
       ├── SkillAgent       → skill detection
       └── SkillGapAgent    → gap analysis + roadmap

Author  : TalentMind AI Team
Version : 1.0.0
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


# ══════════════════════════════════════════════════════════════════
# MODULE-LEVEL HELPER FUNCTIONS
# (These are standalone functions, NOT inside any class)
# ══════════════════════════════════════════════════════════════════

def _normalize_experience_level(level: str) -> str:
    """
    Normalize any experience level string to internal key.

    Handles all UI variations, titles, and display strings.

    Args:
        level: Raw level string from UI or user input

    Returns:
        str: One of: fresher, junior, mid, senior, lead
    """
    level_lower = level.lower().strip()

    level_map = {
        # ── Direct keys ───────────────────────────────────────────
        "fresher": "fresher",
        "junior": "junior",
        "mid": "mid",
        "senior": "senior",
        "lead": "lead",
        # ── UI display strings ────────────────────────────────────
        "fresher (0-1 years)": "fresher",
        "junior (1-2 years)": "junior",
        "mid level (2-5 years)": "mid",
        "mid level": "mid",
        "senior (5-8 years)": "senior",
        "lead (8+ years)": "lead",
        # ── Year ranges ───────────────────────────────────────────
        "0-1": "fresher",
        "1-2": "junior",
        "2-5": "mid",
        "5-8": "senior",
        "8+": "lead",
        # ── Job titles ────────────────────────────────────────────
        "manager": "senior",
        "team lead": "lead",
        "team leader": "lead",
        "principal": "lead",
        "staff": "lead",
        "associate": "junior",
        "intern": "fresher",
        "internship": "fresher",
        "entry": "fresher",
        "entry level": "fresher",
        # ── Numeric ───────────────────────────────────────────────
        "1": "fresher",
        "2": "junior",
        "3": "mid",
        "4": "mid",
        "5": "senior",
    }

    return level_map.get(level_lower, "mid")


def _get_generic_fallback(role: str) -> Dict[str, Any]:
    """
    Generic fallback benchmark when AI generation fails.

    Returns universal professional skills applicable
    to most roles regardless of industry.

    Args:
        role: Job role name for context

    Returns:
        dict: Generic benchmark structure
    """
    return {
        "must_have": [
            "domain knowledge",
            "communication skills",
            "ms office",
            "problem solving",
            "teamwork",
        ],
        "good_to_have": [
            "project management",
            "leadership",
            "time management",
            "analytical thinking",
        ],
        "bonus": [
            "data analysis",
            "digital tools",
            "certifications",
        ],
        "role_description": f"Professional role: {role}",
        "industry": "General",
        "is_dynamic": True,
        "is_fallback": True,
    }


def generate_dynamic_benchmark(
    role: str,
    experience_level: str = "mid",
) -> Dict[str, Any]:
    """
    Generate benchmark for ANY role using Google Gemini AI.

    Called when role is NOT found in static database.
    Uses LLM to generate realistic, role-specific skill
    requirements for any job in any industry.

    Args:
        role            : Any job role name (e.g., "Chef", "Pilot")
        experience_level: Experience level key

    Returns:
        dict: {must_have, good_to_have, bonus, is_dynamic}
    """
    import json

    try:
        from google import genai
        from app.core.settings import get_settings

        settings = get_settings()
        client = genai.Client(api_key=settings.GOOGLE_API_KEY)

        prompt = f"""
You are an expert HR professional and industry specialist
with knowledge of hiring requirements across ALL industries.

Generate realistic skill requirements for this job role:

Role             : {role}
Experience Level : {experience_level}

Provide SPECIFIC skills that employers ACTUALLY require
when hiring for this role at this experience level.
Be industry-specific and practical.

Return ONLY this exact JSON format, no markdown, no explanation:
{{
    "must_have": [
        "skill1", "skill2", "skill3", "skill4", "skill5"
    ],
    "good_to_have": [
        "skill1", "skill2", "skill3", "skill4"
    ],
    "bonus": [
        "skill1", "skill2", "skill3"
    ],
    "role_description": "One line description of this role",
    "industry": "Industry name this role belongs to"
}}

Rules:
- must_have    : 5-8 essential skills (required to get hired)
- good_to_have : 4-6 preferred skills (improve chances)
- bonus        : 2-4 nice-to-have skills (differentiators)
- Be specific to {role} at {experience_level} level
- Use simple, clear skill names
- Include both technical AND soft skills where relevant

Return ONLY valid JSON. No text before or after.
"""

        response = client.models.generate_content(
            model=settings.GEMINI_MODEL,
            contents=prompt,
        )
        response_text = response.text.strip()

        # ── Strip markdown wrappers if present ────────────────────
        if "```json" in response_text:
            response_text = response_text.split("```json")[1]
            response_text = response_text.split("```")[0]
        elif "```" in response_text:
            response_text = response_text.split("```")[1]
            response_text = response_text.split("```")[0]

        result = json.loads(response_text.strip())

        logger.info(
            "Dynamic benchmark generated | role=%s | level=%s",
            role,
            experience_level,
        )

        return {
            "must_have": result.get("must_have", []),
            "good_to_have": result.get("good_to_have", []),
            "bonus": result.get("bonus", []),
            "role_description": result.get(
                "role_description", ""
            ),
            "industry": result.get("industry", "General"),
            "is_dynamic": True,
            "is_fallback": False,
        }

    except Exception as exc:
        logger.warning(
            "Dynamic benchmark failed for '%s': %s",
            role,
            str(exc),
        )
        return _get_generic_fallback(role)


# ══════════════════════════════════════════════════════════════════
# SKILL ANALYZER SERVICE CLASS
# ══════════════════════════════════════════════════════════════════

class SkillAnalyzer:
    """
    Service class for complete skill intelligence operations.

    Orchestrates SkillAnalysisAgent and SkillGapAgent
    to provide full skill analysis and gap detection.

    Supports ANY job role via:
        1. Static database lookup (instant)
        2. Fuzzy role name matching (instant)
        3. Keyword-based domain detection (instant)
        4. AI-powered dynamic generation (any role)
        5. Generic fallback (always works)

    Usage:
        analyzer = SkillAnalyzer()

        # Full pipeline
        result = analyzer.analyze(resume_text, target_role)

        # Gap analysis only
        result = analyzer.analyze_skill_gap(
            resume_text=resume_text,
            target_role="Chef",
            experience_level="mid",
        )
    """

    def __init__(self) -> None:
        """Initialize SkillAnalyzer service."""
        self._skill_agent = None
        self._gap_agent = None
        logger.info("SkillAnalyzer service initialized")

    # ══════════════════════════════════════════════════════════════
    # PRIVATE: LAZY LOADERS
    # ══════════════════════════════════════════════════════════════

    def _get_skill_agent(self):
        """Lazy load SkillAnalysisAgent."""
        if self._skill_agent is None:
            from app.agents.skill_agent import SkillAnalysisAgent
            self._skill_agent = SkillAnalysisAgent()
            logger.info("Loaded: SkillAnalysisAgent")
        return self._skill_agent

    def _get_gap_agent(self):
        """Lazy load SkillGapAgent."""
        if self._gap_agent is None:
            from app.agents.skill_gap_agent import SkillGapAgent
            self._gap_agent = SkillGapAgent()
            logger.info("Loaded: SkillGapAgent")
        return self._gap_agent

    def _get_benchmark(
        self,
        role: str,
        experience_level: str,
    ) -> Dict[str, Any]:
        """
        Get benchmark using priority system.

        Step 1: Static database lookup (instant)
        Step 2: AI dynamic generation (any role)
        Step 3: Generic fallback (always works)

        Args:
            role            : Any job role string
            experience_level: Experience level string

        Returns:
            dict: Benchmark data
        """
        level = _normalize_experience_level(experience_level)

        try:
            from app.utils.industry_benchmarks import get_benchmark
            result = get_benchmark(role, level)
            if result is not None:
                return result
        except Exception as exc:
            logger.warning(
                "Benchmark lookup failed: %s", exc
            )

        # Role not in static DB — use AI to generate relevant benchmarks
        logger.info(
            "Role '%s' not in DB, generating AI benchmark", role
        )
        return generate_dynamic_benchmark(role, level)

    # ══════════════════════════════════════════════════════════════
    # PUBLIC: MAIN ANALYSIS METHODS
    # ══════════════════════════════════════════════════════════════

    def analyze(
        self,
        resume_text: str,
        target_role: str = "General Technology Role",
        parsed_resume: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Run complete skill analysis + gap analysis pipeline.

        Args:
            resume_text  : Raw resume text
            target_role  : Target job role (any role)
            parsed_resume: Optional pre-parsed resume data

        Returns:
            dict: {
                success        : bool
                skill_analysis : dict
                gap_analysis   : dict
                error          : str or None
            }
        """
        if not resume_text or not resume_text.strip():
            return {
                "success": False,
                "error": "No resume text provided.",
                "skill_analysis": {},
                "gap_analysis": {},
            }

        try:
            # Step 1: Skill detection
            skill_result = self.analyze_skills_only(
                resume_text=resume_text,
                target_role=target_role,
            )

            # Step 2: Gap analysis
            gap_result = self.analyze_gaps_only(
                skill_result=skill_result,
                target_role=target_role,
            )

            return {
                "success": True,
                "error": None,
                "skill_analysis": skill_result,
                "gap_analysis": gap_result,
            }

        except Exception as exc:
            logger.error("Full analysis failed: %s", str(exc))
            return {
                "success": False,
                "error": str(exc),
                "skill_analysis": {},
                "gap_analysis": {},
            }

    def analyze_skill_gap(
        self,
        resume_text: str,
        target_role: str = "General Technology Role",
        experience_level: str = "mid",
        job_description: Optional[str] = None,
        industry: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Run skill gap analysis for ANY role in ANY industry.

        Uses AI-powered dynamic benchmark when role is not
        in the static database.

        Args:
            resume_text      : Raw resume text
            target_role      : Any job role (Chef, Pilot, etc.)
            experience_level : Experience level string
            job_description  : Optional JD for better accuracy
            industry         : Optional industry context

        Returns:
            dict: Complete skill gap analysis result
        """
        if not resume_text or not resume_text.strip():
            return self._empty_gap_result(
                "No resume text provided."
            )

        try:
            # ── Normalize experience level ────────────────────────
            normalized_level = _normalize_experience_level(
                experience_level
            )

            logger.info(
                "Skill gap analysis | role=%s | level=%s",
                target_role,
                normalized_level,
            )

            # ── Step 1: Run skill detection ───────────────────────
            skill_result = self.analyze_skills_only(
                resume_text=resume_text,
                target_role=target_role,
            )

            # ── Step 2: Get benchmark (any role) ──────────────────
            benchmark = self._get_benchmark(
                target_role, normalized_level
            )

            # ── Add context to skill result ───────────────────────
            skill_result["benchmark"] = benchmark
            skill_result["is_dynamic_benchmark"] = benchmark.get(
                "is_dynamic", False
            )
            if job_description:
                skill_result["job_description"] = job_description
            if industry:
                skill_result["industry"] = industry

            # ── Step 3: Run gap analysis ──────────────────────────
            gap_agent = self._get_gap_agent()
            gap_result = gap_agent.run({
                "skill_analysis_result": skill_result,
                "target_role": target_role,
                "experience_level": normalized_level,
                "job_description": job_description or "",
                "industry": industry or "",
            })

            # ── Step 4: Add metadata ──────────────────────────────
            gap_result["detected_skills"] = skill_result.get(
                "top_skills", []
            )
            gap_result["experience_level_detected"] = (
                skill_result.get(
                    "experience_level", normalized_level
                )
            )
            gap_result["primary_domain"] = skill_result.get(
                "primary_domain", "general"
            )
            gap_result["benchmark_source"] = (
                "AI Generated"
                if benchmark.get("is_dynamic")
                else "Database"
            )
            if benchmark.get("role_description"):
                gap_result["role_description"] = benchmark[
                    "role_description"
                ]

            return gap_result

        except Exception as exc:
            logger.error(
                "Skill gap analysis failed: %s", str(exc)
            )
            return self._empty_gap_result(str(exc))

    def analyze_skills_only(
        self,
        resume_text: str,
        target_role: str = "General Technology Role",
    ) -> Dict[str, Any]:
        """
        Run skill detection only (no gap analysis).

        Args:
            resume_text: Raw resume text
            target_role: Target job role

        Returns:
            dict: Skill analysis result
        """
        if not resume_text or not resume_text.strip():
            return {
                "success": False,
                "error": "No resume text provided.",
                "total_skills_count": 0,
                "technical_skills": [],
                "top_skills": [],
            }

        try:
            skill_agent = self._get_skill_agent()
            return skill_agent.run({
                "resume_text": resume_text,
                "target_role": target_role,
            })

        except Exception as exc:
            logger.error(
                "Skill detection failed: %s", str(exc)
            )
            return {
                "success": False,
                "error": str(exc),
                "total_skills_count": 0,
                "technical_skills": [],
                "top_skills": [],
            }

    def analyze_gaps_only(
        self,
        skill_result: Dict[str, Any],
        target_role: str = "General Technology Role",
        experience_level: str = "mid",
    ) -> Dict[str, Any]:
        """
        Run gap analysis from existing skill result.

        Args:
            skill_result     : Output from skill analysis
            target_role      : Target job role
            experience_level : Candidate experience level

        Returns:
            dict: Gap analysis result
        """
        try:
            normalized_level = _normalize_experience_level(
                experience_level
            )
            gap_agent = self._get_gap_agent()
            return gap_agent.run({
                "skill_analysis_result": skill_result,
                "target_role": target_role,
                "experience_level": normalized_level,
            })

        except Exception as exc:
            logger.error(
                "Gap analysis failed: %s", str(exc)
            )
            return self._empty_gap_result(str(exc))

    # ══════════════════════════════════════════════════════════════
    # PUBLIC: UTILITY METHODS
    # ══════════════════════════════════════════════════════════════

    def get_supported_roles(self) -> List[str]:
        """
        Get list of all roles in static database.

        Returns:
            list: Role display names
        """
        try:
            from app.utils.industry_benchmarks import (
                get_all_roles,
            )
            return get_all_roles()
        except Exception:
            return [
                "Python Developer",
                "ML Engineer",
                "Full Stack Developer",
                "Data Scientist",
                "DevOps Engineer",
                "AI Engineer",
                "Doctor / Physician",
                "Nurse",
                "Bank Clerk",
                "Financial Analyst",
                "IAS / Civil Services Officer",
                "Fashion Designer",
                "Lawyer / Advocate",
                "HR Manager",
            ]

    def get_experience_levels(self) -> List[str]:
        """
        Get list of experience level display options.

        Returns:
            list: Display strings for UI dropdown
        """
        return [
            "Fresher (0-1 years)",
            "Junior (1-2 years)",
            "Mid Level (2-5 years)",
            "Senior (5-8 years)",
            "Lead (8+ years)",
        ]

    def parse_experience_level(
        self,
        level_display: str,
    ) -> str:
        """
        Convert any level display string to internal key.

        Args:
            level_display: UI display string or any variation

        Returns:
            str: Internal level key
        """
        return _normalize_experience_level(level_display)

    def is_role_in_database(self, role: str) -> bool:
        """
        Check if role exists in static database.

        Useful for UI to show 'AI Generated' badge
        when using dynamic benchmarks.

        Args:
            role: Job role to check

        Returns:
            bool: True if in static database
        """
        try:
            from app.utils.industry_benchmarks import (
                INDUSTRY_BENCHMARKS,
            )
            role_key = (
                role.lower()
                .replace(" ", "_")
                .replace("-", "_")
                .strip()
            )
            return role_key in INDUSTRY_BENCHMARKS
        except Exception:
            return False

    # ══════════════════════════════════════════════════════════════
    # PRIVATE: HELPERS
    # ══════════════════════════════════════════════════════════════

    def _empty_gap_result(
        self,
        error_msg: str = "",
    ) -> Dict[str, Any]:
        """
        Return empty gap result structure.

        Used for error cases to ensure UI never crashes
        due to missing keys.

        Args:
            error_msg: Error description

        Returns:
            dict: Empty result with all required keys
        """
        return {
            "success": False,
            "error": error_msg,
            "overall_readiness_score": 0,
            "readiness_label": "Not Ready",
            "skill_gaps": [],
            "matched_skills": [],
            "critical_gaps_count": 0,
            "high_gaps_count": 0,
            "medium_gaps_count": 0,
            "low_gaps_count": 0,
            "strengths": [],
            "improvement_areas": [],
            "career_advice": "",
            "industry_insight": "",
            "learning_roadmap": {},
            "benchmark_comparison": {},
            "target_role": "",
            "experience_level": "",
            "analyzed_skills_count": 0,
            "total_gaps": 0,
            "detected_skills": [],
            "benchmark_source": "None",
        }


