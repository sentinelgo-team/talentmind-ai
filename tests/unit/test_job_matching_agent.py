"""
Unit tests for JobMatchingAgent
"""

import unittest
from unittest.mock import patch, MagicMock

from app.agents.job_matching_agent import JobMatchingAgent
from app.core.constants import AgentName


class TestJobMatchingAgent(unittest.TestCase):
    """Test cases for JobMatchingAgent"""

    def setUp(self):
        """Set up test fixtures"""
        self.agent = JobMatchingAgent()
        
        self.sample_input = {
            "resume_text": """
            John Doe
            Software Engineer with 3 years of experience in Python, Django, and AWS.
            Built REST APIs and microservices. Experience with PostgreSQL and Docker.
            """,
            "detected_skills": ["Python", "Django", "AWS", "PostgreSQL", "Docker"],
            "experience_level": "Mid-level",
            "primary_domain": "Software Development",
            "target_role": "Senior Python Developer"
        }

    def test_init(self):
        """Test agent initialization"""
        self.assertEqual(self.agent.agent_name, AgentName.JOB_MATCHING)
        self.assertIsNotNone(self.agent._logger)

    @patch('app.agents.base_agent.BaseAgent._call_llm')
    @patch('app.agents.base_agent.BaseAgent._parse_json_response')
    def test_run_success(self, mock_parse_json, mock_call_llm):
        """Test successful job matching"""
        # Mock LLM response
        mock_call_llm.return_value = """
        {
            "job_matches": [
                {
                    "role": "Senior Python Developer",
                    "match_score": 85,
                    "match_label": "Strong Match",
                    "required_skills": ["Python", "Django", "AWS", "PostgreSQL"],
                    "matching_skills": ["Python", "Django", "AWS"],
                    "missing_skills": ["PostgreSQL"],
                    "why_good_fit": "Your Python experience aligns well...",
                    "salary_range": "12-18 LPA",
                    "companies": ["TCS", "Infosys", "Accenture"],
                    "growth_path": "Senior → Lead → Architect"
                }
            ],
            "career_paths": ["Junior → Mid → Senior → Lead"],
            "internship_recs": [],
            "industry_fit": [
                {
                    "industry": "Software Development",
                    "fit_score": 85,
                    "fit_description": "Strong match for software development roles"
                }
            ],
            "salary_range": {"min": 1200000, "max": 1800000, "currency": "INR", "period": "per annum"},
            "next_role_suggestion": "Senior Python Developer",
            "total_matches": 1
        }
        """
        mock_parse_json.return_value = {
            "job_matches": [
                {
                    "role": "Senior Python Developer",
                    "match_score": 85,
                    "match_label": "Strong Match",
                    "required_skills": ["Python", "Django", "AWS", "PostgreSQL"],
                    "matching_skills": ["Python", "Django", "AWS"],
                    "missing_skills": ["PostgreSQL"],
                    "why_good_fit": "Your Python experience aligns well...",
                    "salary_range": "12-18 LPA",
                    "companies": ["TCS", "Infosys", "Accenture"],
                    "growth_path": "Senior → Lead → Architect"
                }
            ],
            "career_paths": ["Junior → Mid → Senior → Lead"],
            "internship_recs": [],
            "industry_fit": [
                {
                    "industry": "Software Development",
                    "fit_score": 85,
                    "fit_description": "Strong match for software development roles"
                }
            ],
            "salary_range": {"min": 1200000, "max": 1800000, "currency": "INR", "period": "per annum"},
            "next_role_suggestion": "Senior Python Developer",
            "total_matches": 1
        }

        result = self.agent.run(self.sample_input)

        # Assertions
        self.assertTrue(result["success"])
        self.assertIsNone(result["error"])
        self.assertEqual(len(result["job_matches"]), 1)
        self.assertEqual(result["job_matches"][0]["role"], "Senior Python Developer")
        self.assertEqual(result["job_matches"][0]["match_score"], 85)
        self.assertEqual(result["total_matches"], 1)
        self.assertEqual(result["next_role_suggestion"], "Senior Python Developer")

    @patch('app.agents.base_agent.BaseAgent._call_llm')
    @patch('app.agents.base_agent.BaseAgent._parse_json_response')
    def test_run_empty_resume(self, mock_parse_json, mock_call_llm):
        """Test handling of empty resume text"""
        input_data = self.sample_input.copy()
        input_data["resume_text"] = ""

        result = self.agent.run(input_data)

        self.assertFalse(result["success"])
        self.assertEqual(result["error"], "No resume text provided.")
        self.assertEqual(result["job_matches"], [])
        self.assertEqual(result["total_matches"], 0)

    @patch('app.agents.base_agent.BaseAgent._call_llm')
    @patch('app.agents.base_agent.BaseAgent._parse_json_response')
    def test_run_parse_failure(self, mock_parse_json, mock_call_llm):
        """Test handling of JSON parse failure"""
        mock_call_llm.return_value = "Invalid JSON response"
        mock_parse_json.return_value = {}

        result = self.agent.run(self.sample_input)

        self.assertFalse(result["success"])
        self.assertEqual(result["error"], "Could not parse job matching results.")
        self.assertEqual(result["job_matches"], [])
        self.assertEqual(result["total_matches"], 0)

    @patch('app.agents.base_agent.BaseAgent._call_llm')
    def test_run_exception(self, mock_call_llm):
        """Test handling of unexpected exceptions"""
        mock_call_llm.side_effect = Exception("API error")

        result = self.agent.run(self.sample_input)

        self.assertFalse(result["success"])
        self.assertEqual(result["error"], "API error")
        self.assertEqual(result["job_matches"], [])
        self.assertEqual(result["total_matches"], 0)


if __name__ == '__main__':
    unittest.main()