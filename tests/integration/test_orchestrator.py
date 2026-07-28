"""
TalentMind AI - Integration Tests: Orchestrator
=================================================
Tests for the AgentOrchestrator workflow.

Author  : TalentMind AI Team
Version : 1.0.0
"""

from __future__ import annotations

import unittest
from unittest.mock import patch, MagicMock

from app.orchestrator.workflow import AgentOrchestrator
from app.core.constants import AgentName


class TestAgentOrchestrator(unittest.TestCase):
    """Tests for AgentOrchestrator."""

    def setUp(self):
        self.orchestrator = AgentOrchestrator()

    def test_init(self):
        """Test orchestrator initializes cleanly."""
        self.assertIsNotNone(self.orchestrator)
        self.assertEqual(self.orchestrator._agents, {})

    def test_run_single_agent_unknown(self):
        """Test running unknown agent returns error."""
        result = self.orchestrator.run_single_agent(
            "NonExistentAgent", {}
        )
        self.assertFalse(result["success"])
        self.assertIn("not available", result["error"])

    @patch("app.agents.resume_agent.ResumeAgent.run")
    def test_run_single_resume_agent(self, mock_run):
        """Test running a single known agent."""
        mock_run.return_value = {
            "success": True,
            "parsed_resume": {"contact_info": {"name": "Test"}},
            "skills_count": 5,
        }

        result = self.orchestrator.run_single_agent(
            AgentName.RESUME,
            {"resume_text": "Test resume content " * 10},
        )

        self.assertTrue(result["success"])
        mock_run.assert_called_once()

    @patch("app.agents.resume_agent.ResumeAgent.run")
    def test_full_analysis_resume_failure_continues(
        self, mock_resume_run
    ):
        """Test that full analysis continues even if resume agent fails."""
        mock_resume_run.return_value = {
            "success": False,
            "error": "API error",
            "parsed_resume": {},
        }

        # Patch all other agents to avoid actual API calls
        with patch(
            "app.agents.ats_agent.ATSAgent.run",
            return_value={"success": False, "error": "skipped"},
        ), patch(
            "app.agents.skill_agent.SkillAnalysisAgent.run",
            return_value={"success": False, "error": "skipped"},
        ), patch(
            "app.agents.skill_gap_agent.SkillGapAgent.run",
            return_value={"success": False, "error": "skipped"},
        ), patch(
            "app.agents.job_matching_agent.JobMatchingAgent.run",
            return_value={"success": False, "error": "skipped"},
        ), patch(
            "app.agents.interview_agent.InterviewAgent.run",
            return_value={"success": False, "error": "skipped"},
        ), patch(
            "app.agents.risk_agent.RiskAnalysisAgent.run",
            return_value={"success": False, "error": "skipped"},
        ), patch(
            "app.agents.recommendation_agent.RecommendationAgent.run",
            return_value={"success": False, "error": "skipped"},
        ), patch(
            "app.agents.ranking_agent.RankingAgent.run",
            return_value={"success": False, "error": "skipped"},
        ), patch(
            "app.agents.reflection_agent.ReflectionAgent.run",
            return_value={"success": False, "error": "skipped"},
        ):
            result = self.orchestrator.run_full_analysis(
                resume_text="Sample resume " * 20,
                target_role="Software Engineer",
            )

        # Pipeline should complete even with all failures
        self.assertIn("resume_result", result)
        self.assertIn("total_time_seconds", result)
        self.assertIn("timings", result)

    def test_progress_callback(self):
        """Test progress callback is invoked."""
        progress_calls = []

        def callback(step, total, msg):
            progress_calls.append((step, total, msg))

        with patch(
            "app.agents.resume_agent.ResumeAgent.run",
            return_value={"success": False, "error": "test"},
        ), patch(
            "app.agents.ats_agent.ATSAgent.run",
            return_value={"success": False, "error": "test"},
        ), patch(
            "app.agents.skill_agent.SkillAnalysisAgent.run",
            return_value={"success": False, "error": "test"},
        ), patch(
            "app.agents.skill_gap_agent.SkillGapAgent.run",
            return_value={"success": False, "error": "test"},
        ), patch(
            "app.agents.job_matching_agent.JobMatchingAgent.run",
            return_value={"success": False, "error": "test"},
        ), patch(
            "app.agents.interview_agent.InterviewAgent.run",
            return_value={"success": False, "error": "test"},
        ), patch(
            "app.agents.risk_agent.RiskAnalysisAgent.run",
            return_value={"success": False, "error": "test"},
        ), patch(
            "app.agents.recommendation_agent.RecommendationAgent.run",
            return_value={"success": False, "error": "test"},
        ), patch(
            "app.agents.ranking_agent.RankingAgent.run",
            return_value={"success": False, "error": "test"},
        ), patch(
            "app.agents.reflection_agent.ReflectionAgent.run",
            return_value={"success": False, "error": "test"},
        ):
            self.orchestrator.run_full_analysis(
                resume_text="Test " * 50,
                progress_callback=callback,
            )

        self.assertEqual(len(progress_calls), 8)
        self.assertEqual(progress_calls[0][0], 1)
        self.assertEqual(progress_calls[-1][0], 8)


if __name__ == "__main__":
    unittest.main()
