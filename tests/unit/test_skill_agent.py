"""
TalentMind AI - Skill Agent Unit Tests
========================================
Author  : TalentMind AI Team
Version : 1.0.0
"""

import pytest
from unittest.mock import patch


class TestSkillAgent:
    """Tests for Skill Analysis Agent."""

    @pytest.fixture
    def mock_agent(self):
        with patch("app.agents.base_agent.genai.Client"):
            from app.agents.skill_agent import SkillAnalysisAgent
            return SkillAnalysisAgent()

    def test_empty_resume_returns_error(self, mock_agent):
        result = mock_agent.run({"resume_text": ""})
        assert result["success"] is False

    def test_no_input_returns_error(self, mock_agent):
        result = mock_agent.run({})
        assert result["success"] is False

    def test_agent_name_correct(self, mock_agent):
        from app.core.constants import AgentName
        assert mock_agent.agent_name == AgentName.SKILL

    def test_parse_valid_skill_response(self, mock_agent):
        response = '''{
            "detected_skills": [
                {"name": "Python", "category": "Programming",
                 "proficiency": "Intermediate", "score": 70}
            ],
            "top_skills"        : ["Python"],
            "skill_gaps"        : ["Docker"],
            "total_skills_count": 1
        }'''
        result = mock_agent._parse_json_response(response)
        assert len(result["detected_skills"]) == 1
        assert result["detected_skills"][0]["name"] == "Python"

    def test_parse_empty_returns_fallback(self, mock_agent):
        result = mock_agent._parse_json_response(
            "", fallback={}
        )
        assert result == {}

    def test_parse_skill_categories(self, mock_agent):
        response = '''{
            "skill_categories": {
                "Programming Languages": ["Python", "Go"],
                "Security Tools"       : ["Burp Suite"]
            }
        }'''
        result = mock_agent._parse_json_response(response)
        assert "Python" in result["skill_categories"][
            "Programming Languages"
        ]

    def test_parse_industry_comparison(self, mock_agent):
        response = '''{
            "industry_comparison": {
                "match_percentage": 65,
                "candidate_has"   : ["Python"],
                "candidate_missing": ["SIEM"]
            }
        }'''
        result = mock_agent._parse_json_response(response)
        assert result["industry_comparison"][
            "match_percentage"
        ] == 65

    def test_parse_proficiency_summary(self, mock_agent):
        response = '''{
            "proficiency_summary": {
                "Intermediate": ["Python", "Linux"],
                "Beginner"    : ["Go"]
            }
        }'''
        result = mock_agent._parse_json_response(response)
        assert "Python" in result[
            "proficiency_summary"
        ]["Intermediate"]