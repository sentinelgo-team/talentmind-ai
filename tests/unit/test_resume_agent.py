"""
TalentMind AI - Resume Agent Unit Tests
=========================================
Updated for google-genai SDK.

Author  : TalentMind AI Team
Version : 1.0.0
"""

import pytest
from unittest.mock import MagicMock, patch


class TestResumeAgentParsing:
    """Tests for resume agent JSON parsing."""

    @pytest.fixture
    def mock_agent(self):
        """Creates agent with mocked GenAI client."""
        with patch(
            "app.agents.base_agent.genai.Client"
        ) as mock_client:
            mock_client.return_value = MagicMock()
            from app.agents.resume_agent import ResumeAgent
            agent = ResumeAgent()
            return agent

    def test_parse_json_clean(self, mock_agent):
        response = '{"skills": ["Python", "Java"]}'
        result   = mock_agent._parse_json_response(response)
        assert result["skills"] == ["Python", "Java"]

    def test_parse_json_with_markdown(self, mock_agent):
        response = '```json\n{"name": "John"}\n```'
        result   = mock_agent._parse_json_response(response)
        assert result["name"] == "John"

    def test_parse_json_empty_returns_fallback(
        self, mock_agent
    ):
        result = mock_agent._parse_json_response(
            "", fallback={"error": "empty"}
        )
        assert result == {"error": "empty"}

    def test_parse_json_invalid_returns_fallback(
        self, mock_agent
    ):
        result = mock_agent._parse_json_response(
            "not json at all", fallback={}
        )
        assert result == {}

    def test_run_empty_text_returns_error(
        self, mock_agent
    ):
        result = mock_agent.run({"resume_text": ""})
        assert result["success"] is False
        assert result["error"] is not None

    def test_run_short_text_returns_error(
        self, mock_agent
    ):
        result = mock_agent.run({"resume_text": "Hi"})
        assert result["success"] is False

    def test_validate_and_build_empty_data(
        self, mock_agent
    ):
        from app.models.resume import ParsedResume
        result = mock_agent._validate_and_build({})
        assert isinstance(result, ParsedResume)
        assert result.skills == []

    def test_validate_and_build_with_skills(
        self, mock_agent
    ):
        data = {
            "skills"      : ["Python", "Django"],
            "contact_info": {"name": "John"},
        }
        result = mock_agent._validate_and_build(data)
        assert "Python" in result.skills
        assert result.contact_info.name == "John"


class TestBaseAgentJsonParsing:
    """Tests for BaseAgent JSON utilities."""

    @pytest.fixture
    def mock_agent(self):
        with patch("app.agents.base_agent.genai.Client"):
            from app.agents.resume_agent import ResumeAgent
            return ResumeAgent()

    def test_extracts_json_from_surrounding_text(
        self, mock_agent
    ):
        response = 'Here is the result: {"key": "value"} done'
        result   = mock_agent._parse_json_response(response)
        assert result["key"] == "value"

    def test_handles_nested_json(self, mock_agent):
        response = '{"outer": {"inner": "value"}}'
        result   = mock_agent._parse_json_response(response)
        assert result["outer"]["inner"] == "value"

    def test_handles_json_array_in_object(
        self, mock_agent
    ):
        response = '{"items": [1, 2, 3]}'
        result   = mock_agent._parse_json_response(response)
        assert result["items"] == [1, 2, 3]