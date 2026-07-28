"""
TalentMind AI - Skill Gap Analysis Agent
==========================================
Agent 05: Detects skill gaps, compares against industry
benchmarks, and generates personalized learning roadmaps.

Responsibilities:
    - Missing Skills Detection
    - Industry Benchmark Comparison
    - Priority Classification (Critical/High/Medium/Low)
    - Learning Roadmap Generation
    - Career Readiness Assessment

Author  : TalentMind AI Team
Version : 1.0.0
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

from app.agents.base_agent import BaseAgent
from app.core.constants import AgentName
from app.prompts.skill_gap_prompts import (
    LEARNING_ROADMAP_PROMPT,
    SKILL_GAP_ANALYSIS_PROMPT,
)
from app.utils.industry_benchmarks import (
    get_benchmark,
    get_all_roles,
)
from app.utils.roadmap_generator import RoadmapGenerator

logger = logging.getLogger(__name__)


class SkillGapAgent(BaseAgent):
    """
    Agent 05 - Skill Gap Analysis Agent

    Performs comprehensive skill gap analysis by comparing
    candidate skills against industry benchmarks and
    generating actionable learning roadmaps.

    Input:
        skill_analysis_result : dict  — Output from SkillAnalysisAgent
        target_role           : str   — Desired job role
        experience_level      : str   — Current experience level

    Output:
        overall_readiness_score  : float — Role readiness 0-100
        readiness_label          : str   — Text label
        skill_gaps               : list  — Detailed gap list
        matched_skills           : list  — Matching skills
        critical_gaps_count      : int   — Count of critical gaps
        learning_roadmap         : dict  — Structured roadmap
        benchmark_comparison     : dict  — Industry comparison
        strengths                : list  — Candidate strengths
        improvement_areas        : list  — Areas to improve
        career_advice            : str   — Personalized advice
    """

    def __init__(self) -> None:
        """Initialize SkillGapAgent."""
        super().__init__(agent_name=AgentName.SKILL_GAP)
        self._roadmap_generator = RoadmapGenerator()
        logger.info("SkillGapAgent initialized")

    def run(
        self,
        input_data: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Execute complete skill gap analysis pipeline.

        Pipeline Steps:
            1. Validate input
            2. Extract skill data from previous agent
            3. Load industry benchmark
            4. Perform rule-based gap detection
            5. LLM deep analysis for priority + context
            6. Generate learning roadmap
            7. Assemble final result

        Args:
            input_data: {
                skill_analysis_result : dict (required)
                target_role           : str  (optional)
                experience_level      : str  (optional)
            }

        Returns:
            dict: Complete skill gap analysis result
        """
        self._log_start(list(input_data.keys()))

        # ── Step 1: Extract inputs ────────────────────────────────
        # FIX: Use "or {}" to safely handle None input
        skill_result = input_data.get("skill_analysis_result") or {}

        target_role = input_data.get(
            "target_role", "General Technology Role"
        )
        experience_level = input_data.get(
            "experience_level",
            skill_result.get("experience_level", "mid"),
        )

        # ── Step 2: Validate ──────────────────────────────────────
        if not skill_result:
            return self._error_result(
                "No skill analysis data provided."
            )

        # ── Step 3: Extract current skills ───────────────────────
        current_skills = self._extract_all_skills(skill_result)

        if not current_skills:
            return self._error_result(
                "No skills found in analysis."
            )

        try:
            # ── Step 4: Load industry benchmark ──────────────────
            logger.info(
                "Loading benchmark | role=%s | level=%s",
                target_role,
                experience_level,
            )
            # Use pre-loaded benchmark from skill_result if available
            benchmark = skill_result.get("benchmark")
            if not benchmark:
                benchmark = get_benchmark(target_role, experience_level)
            if not benchmark:
                from app.services.skill_analyzer import (
                    generate_dynamic_benchmark,
                )
                benchmark = generate_dynamic_benchmark(
                    target_role, experience_level
                )
            must_have = benchmark.get("must_have", [])
            good_to_have = benchmark.get("good_to_have", [])
            bonus = benchmark.get("bonus", [])

            # ── Step 5: Rule-based gap detection ─────────────────
            logger.info("Running rule-based gap detection")
            rule_gaps = self._detect_gaps_rule_based(
                current_skills=current_skills,
                must_have=must_have,
                good_to_have=good_to_have,
                bonus=bonus,
            )

            # Quick readiness score from rules
            quick_score = self._calculate_quick_score(
                current_skills=current_skills,
                must_have=must_have,
                good_to_have=good_to_have,
            )

            # ── Step 6: LLM deep analysis ─────────────────────────
            logger.info("Running LLM gap analysis")
            llm_result = self._run_llm_gap_analysis(
                current_skills=current_skills,
                experience_level=experience_level,
                target_role=target_role,
                primary_domain=skill_result.get(
                    "primary_domain", "general_technology"
                ),
                must_have=must_have,
                good_to_have=good_to_have,
                bonus=bonus,
            )

            # ── Step 7: Generate structured roadmap ──────────────
            logger.info("Generating learning roadmap")
            final_gaps = (
                llm_result.get("skill_gaps", rule_gaps)
                if llm_result else rule_gaps
            )

            roadmap = self._roadmap_generator.generate(
                skill_gaps=final_gaps,
                experience_level=experience_level,
                target_role=target_role,
                current_skills=current_skills,
            )

            # ── Step 8: Assemble result ───────────────────────────
            result = self._assemble_result(
                llm_result=llm_result,
                rule_gaps=rule_gaps,
                roadmap=roadmap,
                current_skills=current_skills,
                benchmark=benchmark,
                target_role=target_role,
                experience_level=experience_level,
                quick_score=quick_score,
            )

            self._log_complete(
                ["skill_gaps", "overall_readiness_score"]
            )
            return result

        except Exception as exc:
            self._log_error(exc)
            return self._error_result(str(exc))

    def _extract_all_skills(
        self,
        skill_result: Dict[str, Any],
    ) -> List[str]:
        """
        Extract flat list of all skills from skill analysis result.

        Combines skills from all categories into one list
        for benchmark comparison.

        Args:
            skill_result: Output from SkillAnalysisAgent

        Returns:
            List of skill names (lowercase)
        """
        all_skills: List[str] = []

        # From top_skills (most reliable)
        top_skills = skill_result.get("top_skills", [])
        if isinstance(top_skills, list):
            all_skills.extend([
                s.lower() if isinstance(s, str)
                else s.get("skill", "").lower()
                for s in top_skills
            ])

        # From technical_skills
        tech_skills = skill_result.get("technical_skills", [])
        for skill in tech_skills:
            if isinstance(skill, dict):
                all_skills.append(
                    skill.get("skill", "").lower()
                )
            elif isinstance(skill, str):
                all_skills.append(skill.lower())

        # From NLP extracted skills (fallback)
        nlp_skills = skill_result.get("nlp_extracted_skills", {})
        if isinstance(nlp_skills, dict):
            for category_skills in nlp_skills.values():
                if isinstance(category_skills, list):
                    all_skills.extend([
                        s.lower() for s in category_skills
                        if isinstance(s, str)
                    ])

        # From detected_skills (list of dicts with 'name' key)
        detected_skills = skill_result.get("detected_skills", [])
        if isinstance(detected_skills, list):
            for skill in detected_skills:
                if isinstance(skill, dict):
                    name = skill.get("name", "").strip()
                    if name:
                        all_skills.append(name.lower())
                elif isinstance(skill, str):
                    all_skills.append(skill.strip().lower())

        # From skill_categories (dict of category -> list of skill names)
        skill_categories = skill_result.get("skill_categories", {})
        if isinstance(skill_categories, dict):
            for category, skills in skill_categories.items():
                if isinstance(skills, list):
                    for skill in skills:
                        if isinstance(skill, str):
                            all_skills.append(skill.strip().lower())

        # Deduplicate while preserving order
        seen = set()
        unique_skills = []
        for skill in all_skills:
            if skill and skill not in seen:
                seen.add(skill)
                unique_skills.append(skill)

        return unique_skills

    def _detect_gaps_rule_based(
        self,
        current_skills: List[str],
        must_have: List[str],
        good_to_have: List[str],
        bonus: List[str],
    ) -> List[Dict[str, Any]]:
        """
        Rule-based gap detection using benchmark comparison.

        Args:
            current_skills: Candidate's current skills
            must_have: Required skills from benchmark
            good_to_have: Preferred skills from benchmark
            bonus: Nice-to-have skills from benchmark

        Returns:
            List of gap dicts with priority
        """
        current_lower = set(s.lower() for s in current_skills)
        gaps: List[Dict[str, Any]] = []

        # Check must-have skills (CRITICAL priority)
        for skill in must_have:
            if not self._skill_matches(skill, current_lower):
                gaps.append({
                    "skill": skill,
                    "priority": "critical",
                    "reason": f"Required for this role",
                    "current_level": "none",
                    "target_level": "intermediate",
                    "source": "benchmark",
                })

        # Check good-to-have skills (HIGH priority)
        for skill in good_to_have:
            if not self._skill_matches(skill, current_lower):
                gaps.append({
                    "skill": skill,
                    "priority": "high",
                    "reason": "Highly preferred by employers",
                    "current_level": "none",
                    "target_level": "beginner",
                    "source": "benchmark",
                })

        # Check bonus skills (LOW priority) — limit to 3
        for skill in bonus[:3]:
            if not self._skill_matches(skill, current_lower):
                gaps.append({
                    "skill": skill,
                    "priority": "low",
                    "reason": "Nice-to-have differentiator",
                    "current_level": "none",
                    "target_level": "beginner",
                    "source": "benchmark",
                })

        return gaps

    def _skill_matches(
        self,
        required_skill: str,
        current_skills: set,
    ) -> bool:
        """
        Check if required skill exists in current skills.

        Uses fuzzy matching to handle skill name variations.

        Args:
            required_skill: Skill to look for
            current_skills: Set of candidate's skills (lowercase)

        Returns:
            bool: True if skill or similar found
        """
        req_lower = required_skill.lower()

        # Direct match
        if req_lower in current_skills:
            return True

        # Partial match
        for current in current_skills:
            if req_lower in current or current in req_lower:
                return True

        # Common aliases
        aliases = {
            "postgresql": ["postgres", "pg"],
            "javascript": ["js", "node.js", "nodejs"],
            "python": ["py"],
            "machine learning": ["ml", "sklearn", "scikit-learn"],
            "kubernetes": ["k8s"],
            "amazon web services": ["aws"],
            "google cloud platform": ["gcp", "google cloud"],
            "microsoft azure": ["azure"],
        }

        for canonical, alias_list in aliases.items():
            if req_lower == canonical:
                if any(a in current_skills for a in alias_list):
                    return True
            if req_lower in alias_list:
                if canonical in current_skills:
                    return True

        return False

    def _calculate_quick_score(
        self,
        current_skills: List[str],
        must_have: List[str],
        good_to_have: List[str],
    ) -> float:
        """
        Calculate quick readiness score from rule-based matching.

        Scoring weights:
            Must-have coverage  : 70%
            Good-to-have        : 30%

        FIX: Empty list returns 0.0 (not full weight)
             No requirements data = no score awarded.

        Args:
            current_skills: Candidate skills
            must_have: Required skills
            good_to_have: Preferred skills

        Returns:
            float: Score 0-100
        """
        current_set = set(s.lower() for s in current_skills)

        # FIX: Empty must_have → 0.0 (not 70.0)
        if must_have:
            must_matched = sum(
                1 for skill in must_have
                if self._skill_matches(skill, current_set)
            )
            must_score = (must_matched / len(must_have)) * 70
        else:
            must_score = 0.0

        # FIX: Empty good_to_have → 0.0 (not 30.0)
        if good_to_have:
            good_matched = sum(
                1 for skill in good_to_have
                if self._skill_matches(skill, current_set)
            )
            good_score = (good_matched / len(good_to_have)) * 30
        else:
            good_score = 0.0

        return round(must_score + good_score, 1)

    def _run_llm_gap_analysis(
        self,
        current_skills: List[str],
        experience_level: str,
        target_role: str,
        primary_domain: str,
        must_have: List[str],
        good_to_have: List[str],
        bonus: List[str],
    ) -> Dict[str, Any]:
        """
        Run LLM-based deep gap analysis.

        Returns empty dict on any failure — agent continues
        with rule-based results as fallback.

        Args:
            current_skills: Candidate skills list
            experience_level: Candidate level
            target_role: Target role
            primary_domain: Detected domain
            must_have: Required skills
            good_to_have: Preferred skills
            bonus: Nice-to-have skills

        Returns:
            dict: LLM analysis or empty dict on failure
        """
        try:
            skills_str = ", ".join(current_skills[:30])
            must_str = ", ".join(must_have)
            good_str = ", ".join(good_to_have)
            bonus_str = ", ".join(bonus)

            prompt = SKILL_GAP_ANALYSIS_PROMPT.format(
                current_skills=skills_str,
                experience_level=experience_level,
                primary_domain=primary_domain,
                target_role=target_role,
                must_have_skills=must_str,
                good_to_have_skills=good_str,
                bonus_skills=bonus_str,
            )

            response = self._call_llm(prompt)
            result = self._parse_json_response(
                response, fallback={}
            )
            return result if result else {}

        except Exception as exc:
            logger.warning(
                "LLM gap analysis failed, using rule-based: %s",
                str(exc),
            )
            return {}

    def _assemble_result(
        self,
        llm_result: Dict[str, Any],
        rule_gaps: List[Dict[str, Any]],
        roadmap: Dict[str, Any],
        current_skills: List[str],
        benchmark: Dict[str, List[str]],
        target_role: str,
        experience_level: str,
        quick_score: float,
    ) -> Dict[str, Any]:
        """
        Assemble final result from all pipeline sources.
        LLM results take priority over rule-based when available.
        """
        # Use LLM score if available, else quick score
        readiness_score = float(
            llm_result.get("overall_readiness_score", quick_score)
        )
        # Always clamp to valid range 0-100
        readiness_score = max(0.0, min(100.0, readiness_score))

        readiness_label = llm_result.get(
            "readiness_label",
            self._get_readiness_label(readiness_score),
        )

        skill_gaps = llm_result.get("skill_gaps", rule_gaps)
        matched_skills = llm_result.get(
            "matched_skills",
            self._get_matched_skills(current_skills, benchmark),
        )

        return {
            "success": True,
            "error": None,
            # ── Readiness ─────────────────────────────────────────
            "overall_readiness_score": readiness_score,
            "readiness_label": readiness_label,
            # ── Gap Analysis ──────────────────────────────────────
            "skill_gaps": skill_gaps,
            "matched_skills": matched_skills,
            "critical_gaps_count": llm_result.get(
                "critical_gaps_count",
                sum(
                    1 for g in rule_gaps
                    if g.get("priority") == "critical"
                ),
            ),
            "high_gaps_count": llm_result.get(
                "high_gaps_count",
                sum(
                    1 for g in rule_gaps
                    if g.get("priority") == "high"
                ),
            ),
            "medium_gaps_count": llm_result.get(
                "medium_gaps_count",
                sum(
                    1 for g in rule_gaps
                    if g.get("priority") == "medium"
                ),
            ),
            "low_gaps_count": llm_result.get(
                "low_gaps_count",
                sum(
                    1 for g in rule_gaps
                    if g.get("priority") == "low"
                ),
            ),
            # ── Insights ──────────────────────────────────────────
            "strengths": llm_result.get("strengths", []),
            "improvement_areas": llm_result.get(
                "improvement_areas", []
            ),
            "career_advice": llm_result.get("career_advice", ""),
            "industry_insight": llm_result.get(
                "industry_insight", ""
            ),
            # ── Roadmap ───────────────────────────────────────────
            "learning_roadmap": roadmap,
            # ── Benchmark ─────────────────────────────────────────
            "benchmark_comparison": {
                "must_have": benchmark.get("must_have", []),
                "good_to_have": benchmark.get("good_to_have", []),
                "bonus": benchmark.get("bonus", []),
            },
            # ── Context ───────────────────────────────────────────
            "target_role": target_role,
            "experience_level": experience_level,
            "analyzed_skills_count": len(current_skills),
            "total_gaps": len(skill_gaps),
        }

    def _get_readiness_label(self, score: float) -> str:
        """Convert numeric score to readiness label."""
        if score > 80:
            return "Ready"
        elif score > 60:
            return "Mostly Ready"
        elif score >= 40:
            return "Partially Ready"
        else:
            return "Not Ready"

    def _get_matched_skills(
        self,
        current_skills: List[str],
        benchmark: Dict[str, List[str]],
    ) -> List[Dict[str, str]]:
        """Build matched skills list from benchmark comparison."""
        current_set = set(s.lower() for s in current_skills)
        matched = []

        all_required = (
            benchmark.get("must_have", []) +
            benchmark.get("good_to_have", [])
        )

        for skill in all_required:
            if self._skill_matches(skill, current_set):
                matched.append({
                    "skill": skill,
                    "proficiency_match": "good",
                    "comment": "Skill found in profile",
                })

        return matched

    def _error_result(self, error_msg: str) -> Dict[str, Any]:
        """Return standardized error result."""
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
            "learning_roadmap": {},
            "benchmark_comparison": {},
            "target_role": "",
            "experience_level": "",
            "analyzed_skills_count": 0,
            "total_gaps": 0,
        }