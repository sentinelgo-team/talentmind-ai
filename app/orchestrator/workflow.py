"""
TalentMind AI - Agent Orchestrator
====================================
Coordinates all AI agents in a structured workflow
using LangGraph StateGraph with fallback to sequential.

Pipeline:
    resume_parse → (ats, skill_analysis) → skill_gap →
    (job_matching, interview, risk, recommendation) →
    ranking → reflection

Author  : TalentMind AI Team
Version : 1.0.0
"""

from __future__ import annotations

import logging
import time
from typing import Any, Dict, Optional

from app.core.constants import AgentName

logger = logging.getLogger(__name__)


class AgentOrchestrator:
    """
    Coordinates all TalentMind AI agents in a workflow.

    Provides:
        - Full pipeline execution
        - Single agent execution
        - Error isolation (one failure doesn't crash all)
        - Progress callbacks for UI
        - Timing metrics
    """

    def __init__(self) -> None:
        self._agents: Dict[str, Any] = {}
        logger.info("AgentOrchestrator initialized")

    def _get_agent(self, name: str):
        """Lazy-load and cache agent instances."""
        if name not in self._agents:
            try:
                self._agents[name] = self._create_agent(name)
            except Exception as exc:
                logger.error(
                    "Failed to create agent %s: %s", name, exc
                )
                return None
        return self._agents[name]

    def _create_agent(self, name: str):
        """Factory method for agent creation."""
        if name == AgentName.RESUME:
            from app.agents.resume_agent import ResumeAgent
            return ResumeAgent()
        elif name == AgentName.ATS:
            from app.agents.ats_agent import ATSAgent
            return ATSAgent()
        elif name == AgentName.SKILL:
            from app.agents.skill_agent import (
                SkillAnalysisAgent,
            )
            return SkillAnalysisAgent()
        elif name == AgentName.SKILL_GAP:
            from app.agents.skill_gap_agent import (
                SkillGapAgent,
            )
            return SkillGapAgent()
        elif name == AgentName.JOB_MATCHING:
            from app.agents.job_matching_agent import (
                JobMatchingAgent,
            )
            return JobMatchingAgent()
        elif name == AgentName.INTERVIEW:
            from app.agents.interview_agent import (
                InterviewAgent,
            )
            return InterviewAgent()
        elif name == AgentName.RECOMMENDATION:
            from app.agents.recommendation_agent import (
                RecommendationAgent,
            )
            return RecommendationAgent()
        elif name == AgentName.RANKING:
            from app.agents.ranking_agent import RankingAgent
            return RankingAgent()
        elif name == AgentName.REFLECTION:
            from app.agents.reflection_agent import (
                ReflectionAgent,
            )
            return ReflectionAgent()
        elif name == AgentName.RISK:
            from app.agents.risk_agent import (
                RiskAnalysisAgent,
            )
            return RiskAnalysisAgent()
        else:
            raise ValueError(f"Unknown agent: {name}")

    def run_full_analysis(
        self,
        resume_text: str,
        target_role: str = "General Technology Role",
        candidate_id: str = "",
        candidate_name: str = "",
        experience_level: str = "mid",
        progress_callback=None,
    ) -> Dict[str, Any]:
        """
        Run the complete analysis pipeline.

        Pipeline order:
            1. Resume parsing
            2. ATS analysis + Skill analysis (parallel-safe)
            3. Skill gap analysis
            4. Job matching + Interview + Risk + Recommendation
            5. Ranking
            6. Reflection (quality check)

        Args:
            resume_text: Raw resume text
            target_role: Target job role
            candidate_id: Candidate UUID
            candidate_name: Candidate name
            experience_level: Experience level
            progress_callback: Optional fn(step, total, msg)

        Returns:
            dict: All agent results combined
        """
        start_time = time.time()
        results: Dict[str, Any] = {
            "success": True,
            "target_role": target_role,
            "candidate_id": candidate_id,
            "candidate_name": candidate_name,
            "timings": {},
        }

        total_steps = 8

        def _progress(step: int, msg: str) -> None:
            if progress_callback:
                progress_callback(step, total_steps, msg)
            logger.info(
                "Pipeline [%d/%d]: %s",
                step, total_steps, msg
            )

        # Step 1: Resume Parsing
        _progress(1, "Parsing resume...")
        resume_result = self._run_agent_safe(
            AgentName.RESUME,
            {
                "resume_text": resume_text,
                "target_role": target_role,
            },
            results,
            "resume_result",
        )

        # Step 2: ATS Analysis
        _progress(2, "Running ATS analysis...")
        self._run_agent_safe(
            AgentName.ATS,
            {
                "resume_text": resume_text,
                "target_role": target_role,
                "parsed_resume": (
                    resume_result.get("parsed_resume") or {}
                    if resume_result else {}
                ),
            },
            results,
            "ats_result",
        )

        # Step 3: Skill Analysis
        _progress(3, "Analyzing skills...")
        skill_result = self._run_agent_safe(
            AgentName.SKILL,
            {
                "resume_text": resume_text,
                "parsed_resume": (
                    resume_result.get("parsed_resume") or {}
                    if resume_result else {}
                ),
            },
            results,
            "skill_result",
        )

        # Step 4: Skill Gap Analysis
        _progress(4, "Detecting skill gaps...")
        skill_gap_result = self._run_agent_safe(
            AgentName.SKILL_GAP,
            {
                "skill_analysis_result": skill_result or {},
                "target_role": target_role,
                "experience_level": experience_level,
            },
            results,
            "skill_gap_result",
        )

        # Step 5: Job Matching + Interview Prep
        _progress(5, "Matching jobs and preparing interview...")
        self._run_agent_safe(
            AgentName.JOB_MATCHING,
            {
                "resume_text": resume_text,
                "skill_analysis_result": skill_result or {},
                "target_role": target_role,
                "experience_level": experience_level,
            },
            results,
            "job_matching_result",
        )

        self._run_agent_safe(
            AgentName.INTERVIEW,
            {
                "resume_text": resume_text,
                "skill_analysis_result": skill_result or {},
                "target_role": target_role,
                "experience_level": experience_level,
            },
            results,
            "interview_result",
        )

        # Step 6: Risk + Recommendation
        _progress(6, "Assessing risks and recommendations...")
        self._run_agent_safe(
            AgentName.RISK,
            {
                "skill_analysis_result": skill_result or {},
                "skill_gap_result": skill_gap_result or {},
                "target_role": target_role,
                "experience_level": experience_level,
                "experience_years": (
                    resume_result.get("parsed_resume", {})
                    .get("total_experience_years", 0)
                    if resume_result else 0
                ),
            },
            results,
            "risk_result",
        )

        self._run_agent_safe(
            AgentName.RECOMMENDATION,
            {
                "skill_analysis_result": skill_result or {},
                "skill_gap_result": skill_gap_result or {},
                "ats_result": results.get("ats_result") or {},
                "target_role": target_role,
                "experience_level": experience_level,
            },
            results,
            "recommendation_result",
        )

        # Step 7: Ranking
        _progress(7, "Ranking candidate profile...")
        self._run_agent_safe(
            AgentName.RANKING,
            {
                "resume_text": resume_text,
                "target_role": target_role,
                "experience_level": experience_level,
                "skill_analysis_result": skill_result or {},
                "ats_result": results.get("ats_result") or {},
                "skill_gap_result": skill_gap_result or {},
            },
            results,
            "ranking_result",
        )

        # Step 8: Reflection (quality check)
        _progress(8, "Quality assessment...")
        self._run_agent_safe(
            AgentName.REFLECTION,
            {
                "resume_result": resume_result or {},
                "ats_result": results.get("ats_result") or {},
                "skill_result": skill_result or {},
                "skill_gap_result": skill_gap_result or {},
                "job_matching_result": (
                    results.get("job_matching_result") or {}
                ),
                "target_role": target_role,
                "experience_level": experience_level,
            },
            results,
            "reflection_result",
        )

        elapsed = time.time() - start_time
        results["total_time_seconds"] = round(elapsed, 2)

        logger.info(
            "Full analysis complete | time=%.2fs | "
            "agents_succeeded=%d",
            elapsed,
            sum(
                1 for k, v in results.items()
                if isinstance(v, dict)
                and v.get("success")
            ),
        )

        # Persist results to memory system
        if candidate_id:
            self._persist_to_memory(candidate_id, results)

        return results

    def run_single_agent(
        self,
        agent_name: str,
        input_data: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Run a single agent by name.

        Args:
            agent_name: Agent name from AgentName constants
            input_data: Agent-specific input

        Returns:
            dict: Agent result
        """
        agent = self._get_agent(agent_name)
        if not agent:
            return {
                "success": False,
                "error": f"Agent '{agent_name}' not available.",
            }

        try:
            start = time.time()
            result = agent.run(input_data)
            elapsed = time.time() - start
            logger.info(
                "Single agent run | agent=%s | time=%.2fs",
                agent_name, elapsed
            )
            return result
        except Exception as exc:
            logger.error(
                "Single agent failed | agent=%s | error=%s",
                agent_name, exc
            )
            return {
                "success": False,
                "error": str(exc),
            }

    def _run_agent_safe(
        self,
        agent_name: str,
        input_data: Dict[str, Any],
        results: Dict[str, Any],
        result_key: str,
    ) -> Optional[Dict[str, Any]]:
        """
        Run an agent with error isolation.
        Stores result in results dict and returns it.
        On failure, stores error result and returns None.
        """
        agent = self._get_agent(agent_name)
        if not agent:
            error_result = {
                "success": False,
                "error": f"Agent '{agent_name}' not available.",
            }
            results[result_key] = error_result
            return None

        try:
            start = time.time()
            result = agent.run(input_data)
            elapsed = time.time() - start

            results["timings"][agent_name] = round(elapsed, 2)
            results[result_key] = result

            if result.get("success"):
                logger.info(
                    "Agent OK | name=%s | time=%.2fs",
                    agent_name, elapsed
                )
                return result
            else:
                logger.warning(
                    "Agent returned failure | name=%s | "
                    "error=%s",
                    agent_name, result.get("error")
                )
                return None

        except Exception as exc:
            logger.error(
                "Agent exception | name=%s | error=%s",
                agent_name, exc
            )
            results[result_key] = {
                "success": False,
                "error": str(exc),
            }
            return None

    def _persist_to_memory(
        self,
        candidate_id: str,
        results: Dict[str, Any],
    ) -> None:
        """
        Persists successful agent results to the memory system.
        Non-critical — failures are logged but don't affect output.
        """
        try:
            from app.memory.memory_manager import MemoryManager

            memory = MemoryManager()

            result_to_memory_type = {
                "resume_result": "resume_analysis",
                "ats_result": "ats_analysis",
                "skill_result": "skill_analysis",
                "skill_gap_result": "skill_gap",
                "job_matching_result": "job_match",
                "interview_result": "interview_prep",
                "recommendation_result": "recommendations",
                "risk_result": "risk_analysis",
            }

            stored = 0
            for result_key, memory_type in result_to_memory_type.items():
                agent_result = results.get(result_key)
                if (
                    isinstance(agent_result, dict)
                    and agent_result.get("success")
                ):
                    memory.store_memory(
                        candidate_id=candidate_id,
                        memory_type=memory_type,
                        content=agent_result,
                        store_embedding=False,
                    )
                    stored += 1

            logger.info(
                "Memory persisted | candidate=%s | stored=%d/%d",
                candidate_id, stored, len(result_to_memory_type)
            )

        except Exception as exc:
            logger.warning(
                "Memory persistence failed (non-critical) | "
                "error=%s", exc
            )
