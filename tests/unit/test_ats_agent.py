"""
TalentMind AI - ATS Agent Unit Tests
=======================================
Author  : TalentMind AI Team
Version : 1.0.0
"""

import pytest
from unittest.mock import MagicMock, patch


class TestATSAgent:
    """Tests for ATS Agent."""

    @pytest.fixture
    def mock_agent(self):
        with patch("app.agents.base_agent.genai.Client"):
            from app.agents.ats_agent import ATSAgent
            return ATSAgent()

    def test_empty_resume_returns_error(self, mock_agent):
        result = mock_agent.run({"resume_text": ""})
        assert result["success"] is False
        assert result["ats_score"] == 0

    def test_score_label_excellent(self, mock_agent):
        label = mock_agent._get_score_label(90)
        assert label == "Excellent"

    def test_score_label_good(self, mock_agent):
        label = mock_agent._get_score_label(75)
        assert label == "Good"

    def test_score_label_average(self, mock_agent):
        label = mock_agent._get_score_label(60)
        assert label == "Average"

    def test_score_label_poor(self, mock_agent):
        label = mock_agent._get_score_label(30)
        assert label == "Needs Improvement"

    def test_score_label_boundary_excellent(self, mock_agent):
        label = mock_agent._get_score_label(85)
        assert label == "Excellent"

    def test_score_label_boundary_good(self, mock_agent):
        label = mock_agent._get_score_label(70)
        assert label == "Good"

    def test_parse_valid_ats_response(self, mock_agent):
        response = '''{
            "overall_score": 75,
            "score_breakdown": {
                "keyword_score": 70,
                "format_score": 80
            },
            "strengths": ["Good skills"],
            "weaknesses": ["No experience"],
            "ats_suggestions": ["Add more keywords"]
        }'''
        result = mock_agent._parse_json_response(response)
        assert result["overall_score"] == 75
        assert result["score_breakdown"]["keyword_score"] == 70

    def test_parse_empty_returns_fallback(self, mock_agent):
        result = mock_agent._parse_json_response(
            "", fallback={"overall_score": 0}
        )
        assert result["overall_score"] == 0

    def test_run_without_resume_text(self, mock_agent):
        result = mock_agent.run({})
        assert result["success"] is False

    def test_agent_name_correct(self, mock_agent):
        assert mock_agent.agent_name == "ATSAgent"