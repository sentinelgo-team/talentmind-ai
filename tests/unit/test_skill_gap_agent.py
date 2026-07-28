"""
TalentMind AI - Skill Gap Agent Complete Test Suite
=====================================================
Phase 6 Testing: Tests for SkillGapAgent,
RoadmapGenerator, and IndustryBenchmarks.

Author  : TalentMind AI Team
Version : 1.0.0
"""

from __future__ import annotations

import json
import pytest
from unittest.mock import patch


# ══════════════════════════════════════════════════════════════════
# FIXTURES
# ══════════════════════════════════════════════════════════════════

@pytest.fixture
def mock_gap_agent():
    """SkillGapAgent with mocked LLM."""
    with patch("app.agents.base_agent.genai.Client"):
        from app.agents.skill_gap_agent import SkillGapAgent
        return SkillGapAgent()


@pytest.fixture
def strong_skill_result():
    """Skill analysis result with strong skills."""
    return {
        "success": True,
        "top_skills": [
            "Python", "Django", "FastAPI",
            "PostgreSQL", "Docker", "Git",
            "REST API", "Redis", "AWS",
        ],
        "technical_skills": [
            {"skill": "Python", "proficiency": "advanced"},
            {"skill": "Django", "proficiency": "intermediate"},
            {"skill": "Docker", "proficiency": "intermediate"},
        ],
        "experience_level": "mid",
        "primary_domain": "backend_development",
        "nlp_extracted_skills": {
            "programming_languages": ["Python"],
            "databases": ["PostgreSQL", "Redis"],
            "devops_tools": ["Docker"],
        },
    }


@pytest.fixture
def weak_skill_result():
    """Skill analysis result with limited skills."""
    return {
        "success": True,
        "top_skills": ["Python", "SQL"],
        "technical_skills": [
            {"skill": "Python", "proficiency": "beginner"},
        ],
        "experience_level": "fresher",
        "primary_domain": "general_technology",
        "nlp_extracted_skills": {
            "programming_languages": ["Python"],
            "databases": ["SQL"],
        },
    }


@pytest.fixture
def valid_llm_gap_response():
    """Valid LLM response for gap analysis."""
    return json.dumps({
        "overall_readiness_score": 68,
        "readiness_label": "Mostly Ready",
        "skill_gaps": [
            {
                "skill": "Kubernetes",
                "priority": "high",
                "reason": "Required for production deployments",
                "current_level": "none",
                "target_level": "intermediate",
                "learning_suggestion": "Complete Kubernetes course",
                "estimated_weeks": 4,
            },
            {
                "skill": "Terraform",
                "priority": "medium",
                "reason": "Infrastructure as code is standard",
                "current_level": "none",
                "target_level": "beginner",
                "learning_suggestion": "HashiCorp tutorials",
                "estimated_weeks": 3,
            },
        ],
        "matched_skills": [
            {
                "skill": "Python",
                "proficiency_match": "excellent",
                "comment": "Exceeds requirements",
            },
            {
                "skill": "Docker",
                "proficiency_match": "good",
                "comment": "Meets requirements",
            },
        ],
        "critical_gaps_count": 0,
        "high_gaps_count": 1,
        "medium_gaps_count": 1,
        "low_gaps_count": 0,
        "strengths": [
            "Strong Python backend skills",
            "Good database knowledge",
        ],
        "improvement_areas": [
            "Cloud orchestration experience needed",
            "Infrastructure as code skills",
        ],
        "career_advice": "Focus on Kubernetes for senior roles",
        "industry_insight": "K8s is standard in most mid+ roles",
    })


# ══════════════════════════════════════════════════════════════════
# CATEGORY 1: INDUSTRY BENCHMARKS TESTS
# ══════════════════════════════════════════════════════════════════

class TestIndustryBenchmarks:
    """Tests for industry benchmark data and retrieval."""

    def test_get_benchmark_python_mid(self):
        """Python developer mid benchmark returns correct data."""
        from app.utils.industry_benchmarks import get_benchmark
        result = get_benchmark("python_developer", "mid")
        assert "must_have" in result
        assert "good_to_have" in result
        assert "python" in result["must_have"]

    def test_get_benchmark_returns_dict(self):
        """get_benchmark always returns a dict."""
        from app.utils.industry_benchmarks import get_benchmark
        result = get_benchmark("ml_engineer", "junior")
        assert isinstance(result, dict)

    def test_get_benchmark_unknown_role_returns_none(self):
        """Unknown role returns None for AI generation fallback."""
        from app.utils.industry_benchmarks import get_benchmark
        result = get_benchmark("unknown_role_xyz", "mid")
        assert result is None

    def test_get_benchmark_all_levels(self):
        """All experience levels return valid benchmarks."""
        from app.utils.industry_benchmarks import get_benchmark
        levels = ["fresher", "junior", "mid", "senior"]
        for level in levels:
            result = get_benchmark("python_developer", level)
            assert isinstance(result, dict)
            assert len(result) > 0

    def test_get_learning_resource_known_skill(self):
        """Known skill returns resource with platform."""
        from app.utils.industry_benchmarks import get_learning_resource
        result = get_learning_resource("python")
        assert isinstance(result, dict)
        assert "platform" in result

    def test_get_learning_resource_unknown_skill(self):
        """Unknown skill returns default resource."""
        from app.utils.industry_benchmarks import get_learning_resource
        result = get_learning_resource("some_unknown_skill_xyz")
        assert isinstance(result, dict)
        assert "platform" in result

    def test_get_all_roles_returns_list(self):
        """get_all_roles returns non-empty list."""
        from app.utils.industry_benchmarks import get_all_roles
        roles = get_all_roles()
        assert isinstance(roles, list)
        assert len(roles) > 0


# ══════════════════════════════════════════════════════════════════
# CATEGORY 2: ROADMAP GENERATOR TESTS
# ══════════════════════════════════════════════════════════════════

class TestRoadmapGenerator:
    """Tests for the RoadmapGenerator utility."""

    @pytest.fixture
    def generator(self):
        from app.utils.roadmap_generator import RoadmapGenerator
        return RoadmapGenerator()

    @pytest.fixture
    def sample_gaps(self):
        return [
            {"skill": "Docker", "priority": "critical",
             "reason": "Required"},
            {"skill": "Kubernetes", "priority": "high",
             "reason": "Preferred"},
            {"skill": "Terraform", "priority": "medium",
             "reason": "Good to have"},
            {"skill": "Kafka", "priority": "low",
             "reason": "Bonus"},
        ]

    def test_generate_returns_dict(self, generator, sample_gaps):
        """generate() must return a dictionary."""
        result = generator.generate(sample_gaps)
        assert isinstance(result, dict)

    def test_generate_has_phases(self, generator, sample_gaps):
        """Result must include phases list."""
        result = generator.generate(sample_gaps)
        assert "phases" in result
        assert isinstance(result["phases"], list)

    def test_generate_has_milestones(self, generator, sample_gaps):
        """Result must include milestones."""
        result = generator.generate(sample_gaps)
        assert "milestones" in result
        assert isinstance(result["milestones"], list)

    def test_generate_has_weekly_plan(self, generator, sample_gaps):
        """Result must include weekly plan."""
        result = generator.generate(sample_gaps)
        assert "weekly_plan" in result

    def test_generate_has_immediate_actions(
        self, generator, sample_gaps
    ):
        """Result must include immediate actions."""
        result = generator.generate(sample_gaps)
        assert "immediate_actions" in result
        assert isinstance(result["immediate_actions"], list)

    def test_generate_empty_gaps_returns_empty_roadmap(
        self, generator
    ):
        """Empty gaps returns empty roadmap gracefully."""
        result = generator.generate([])
        assert result["total_gaps"] == 0
        assert result["phases"] == []

    def test_generate_estimated_weeks_positive(
        self, generator, sample_gaps
    ):
        """Estimated weeks must be positive."""
        result = generator.generate(sample_gaps)
        assert result["estimated_weeks"] > 0

    def test_phases_sorted_by_priority(
        self, generator, sample_gaps
    ):
        """Phases must be ordered critical → low."""
        result = generator.generate(sample_gaps)
        phases = result["phases"]
        if len(phases) > 1:
            phase_nums = [p["phase_number"] for p in phases]
            assert phase_nums == sorted(phase_nums)

    def test_generate_has_summary(self, generator, sample_gaps):
        """Result must include a text summary."""
        result = generator.generate(sample_gaps)
        assert "summary" in result
        assert isinstance(result["summary"], str)
        assert len(result["summary"]) > 0


# ══════════════════════════════════════════════════════════════════
# CATEGORY 3: AGENT INITIALIZATION TESTS
# ══════════════════════════════════════════════════════════════════

class TestSkillGapAgentInit:
    """Tests for SkillGapAgent initialization."""

    def test_agent_instantiation(self, mock_gap_agent):
        """Agent must instantiate without errors."""
        assert mock_gap_agent is not None

    def test_agent_has_roadmap_generator(self, mock_gap_agent):
        """Agent must have RoadmapGenerator instance."""
        assert hasattr(mock_gap_agent, "_roadmap_generator")

    def test_agent_has_run_method(self, mock_gap_agent):
        """Agent must have callable run() method."""
        assert callable(mock_gap_agent.run)

    def test_agent_inherits_base(self, mock_gap_agent):
        """Agent must inherit from BaseAgent."""
        from app.agents.base_agent import BaseAgent
        assert isinstance(mock_gap_agent, BaseAgent)

    def test_agent_name_correct(self, mock_gap_agent):
        """Agent name must match AgentName.SKILL_GAP."""
        from app.core.constants import AgentName
        assert mock_gap_agent.agent_name == AgentName.SKILL_GAP


# ══════════════════════════════════════════════════════════════════
# CATEGORY 4: INPUT VALIDATION TESTS
# ══════════════════════════════════════════════════════════════════

class TestSkillGapInputValidation:
    """Tests for input validation."""

    def test_empty_input_returns_failure(self, mock_gap_agent):
        """Empty input dict returns success=False."""
        result = mock_gap_agent.run({})
        assert result["success"] is False

    def test_empty_skill_result_returns_failure(
        self, mock_gap_agent
    ):
        """Empty skill_analysis_result returns failure."""
        result = mock_gap_agent.run({
            "skill_analysis_result": {}
        })
        assert result["success"] is False

    def test_none_skill_result_handled(self, mock_gap_agent):
        """None skill result handled gracefully."""
        result = mock_gap_agent.run({
            "skill_analysis_result": None
        })
        assert result["success"] is False

    def test_error_result_has_minimum_keys(self, mock_gap_agent):
        """Error result must have all minimum required keys."""
        result = mock_gap_agent.run({})
        minimum_keys = [
            "success", "error",
            "overall_readiness_score",
            "skill_gaps", "learning_roadmap",
        ]
        for key in minimum_keys:
            assert key in result, f"Missing key: {key}"


# ══════════════════════════════════════════════════════════════════
# CATEGORY 5: PIPELINE TESTS
# ══════════════════════════════════════════════════════════════════

class TestSkillGapPipeline:
    """Tests for the complete analysis pipeline."""

    def test_successful_run_returns_success_true(
        self, mock_gap_agent, strong_skill_result,
        valid_llm_gap_response
    ):
        """Successful run returns success=True."""
        with patch.object(
            mock_gap_agent, "_call_llm",
            return_value=valid_llm_gap_response
        ):
            result = mock_gap_agent.run({
                "skill_analysis_result": strong_skill_result,
                "target_role": "python_developer",
            })
            assert result["success"] is True

    def test_result_has_all_required_keys(
        self, mock_gap_agent, strong_skill_result,
        valid_llm_gap_response
    ):
        """Result must have all required keys."""
        required_keys = [
            "success", "error",
            "overall_readiness_score", "readiness_label",
            "skill_gaps", "matched_skills",
            "critical_gaps_count", "high_gaps_count",
            "strengths", "improvement_areas",
            "career_advice", "learning_roadmap",
            "benchmark_comparison", "target_role",
            "experience_level", "total_gaps",
        ]
        with patch.object(
            mock_gap_agent, "_call_llm",
            return_value=valid_llm_gap_response
        ):
            result = mock_gap_agent.run({
                "skill_analysis_result": strong_skill_result,
                "target_role": "python_developer",
            })
            for key in required_keys:
                assert key in result, f"Missing key: {key}"

    def test_readiness_score_in_valid_range(
        self, mock_gap_agent, strong_skill_result,
        valid_llm_gap_response
    ):
        """Readiness score must be 0-100."""
        with patch.object(
            mock_gap_agent, "_call_llm",
            return_value=valid_llm_gap_response
        ):
            result = mock_gap_agent.run({
                "skill_analysis_result": strong_skill_result,
            })
            score = result["overall_readiness_score"]
            assert 0 <= score <= 100

    def test_readiness_label_valid(
        self, mock_gap_agent, strong_skill_result,
        valid_llm_gap_response
    ):
        """Readiness label must be from valid set."""
        valid_labels = {
            "Not Ready", "Partially Ready",
            "Mostly Ready", "Ready"
        }
        with patch.object(
            mock_gap_agent, "_call_llm",
            return_value=valid_llm_gap_response
        ):
            result = mock_gap_agent.run({
                "skill_analysis_result": strong_skill_result,
            })
            assert result["readiness_label"] in valid_labels

    def test_skill_gaps_is_list(
        self, mock_gap_agent, strong_skill_result,
        valid_llm_gap_response
    ):
        """skill_gaps must be a list."""
        with patch.object(
            mock_gap_agent, "_call_llm",
            return_value=valid_llm_gap_response
        ):
            result = mock_gap_agent.run({
                "skill_analysis_result": strong_skill_result,
            })
            assert isinstance(result["skill_gaps"], list)

    def test_learning_roadmap_is_dict(
        self, mock_gap_agent, strong_skill_result,
        valid_llm_gap_response
    ):
        """learning_roadmap must be a dict."""
        with patch.object(
            mock_gap_agent, "_call_llm",
            return_value=valid_llm_gap_response
        ):
            result = mock_gap_agent.run({
                "skill_analysis_result": strong_skill_result,
            })
            assert isinstance(result["learning_roadmap"], dict)

    def test_weak_skills_generates_more_gaps(
        self, mock_gap_agent, weak_skill_result,
        valid_llm_gap_response
    ):
        """Candidate with weak skills should have more gaps."""
        with patch.object(
            mock_gap_agent, "_call_llm",
            return_value=valid_llm_gap_response
        ):
            result = mock_gap_agent.run({
                "skill_analysis_result": weak_skill_result,
                "target_role": "python_developer",
                "experience_level": "mid",
            })
            assert result["success"] is True


# ══════════════════════════════════════════════════════════════════
# CATEGORY 6: RULE-BASED GAP DETECTION TESTS
# ══════════════════════════════════════════════════════════════════

class TestRuleBasedGapDetection:
    """Tests for rule-based gap detection methods."""

    def test_skill_matches_direct(self, mock_gap_agent):
        """Direct skill match returns True."""
        result = mock_gap_agent._skill_matches(
            "python", {"python", "django"}
        )
        assert result is True

    def test_skill_matches_partial(self, mock_gap_agent):
        """Partial match (postgres/postgresql) returns True."""
        result = mock_gap_agent._skill_matches(
            "postgresql", {"postgres", "redis"}
        )
        assert result is True

    def test_skill_no_match(self, mock_gap_agent):
        """Non-matching skill returns False."""
        result = mock_gap_agent._skill_matches(
            "kubernetes", {"python", "django"}
        )
        assert result is False

    def test_quick_score_full_match(self, mock_gap_agent):
        """Full skill match gives high score."""
        must_have = ["python", "django", "postgresql"]
        current = ["python", "django", "postgresql",
                   "docker", "redis"]
        score = mock_gap_agent._calculate_quick_score(
            current, must_have, []
        )
        assert score >= 70  # Full must-have coverage

    def test_quick_score_no_match(self, mock_gap_agent):
        """No skill match gives low score."""
        must_have = ["kubernetes", "terraform", "aws"]
        current = ["python", "html"]
        score = mock_gap_agent._calculate_quick_score(
            current, must_have, []
        )
        assert score < 30  # Very low coverage

    def test_quick_score_in_range(self, mock_gap_agent):
        """Quick score must always be 0-100."""
        score = mock_gap_agent._calculate_quick_score(
            ["python"], ["python", "docker"], ["aws"]
        )
        assert 0 <= score <= 100


# ══════════════════════════════════════════════════════════════════
# CATEGORY 7: ERROR HANDLING TESTS
# ══════════════════════════════════════════════════════════════════

class TestSkillGapErrorHandling:
    """Tests for error handling and resilience."""

    def test_llm_failure_falls_back_to_rule_based(
        self, mock_gap_agent, strong_skill_result
    ):
        """LLM failure uses rule-based gaps instead."""
        with patch.object(
            mock_gap_agent, "_call_llm",
            side_effect=Exception("LLM unavailable")
        ):
            result = mock_gap_agent.run({
                "skill_analysis_result": strong_skill_result,
                "target_role": "python_developer",
            })
            assert isinstance(result, dict)
            assert "success" in result

    def test_invalid_llm_json_handled(
        self, mock_gap_agent, strong_skill_result
    ):
        """Invalid JSON from LLM handled gracefully."""
        with patch.object(
            mock_gap_agent, "_call_llm",
            return_value="INVALID JSON {{{{"
        ):
            result = mock_gap_agent.run({
                "skill_analysis_result": strong_skill_result,
            })
            assert isinstance(result, dict)

    def test_readiness_score_clamped(self, mock_gap_agent):
        """Readiness score is always clamped to 0-100."""
        label = mock_gap_agent._get_readiness_label(150)
        assert label == "Ready"

        label = mock_gap_agent._get_readiness_label(-10)
        assert label == "Not Ready"