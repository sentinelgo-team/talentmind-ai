"""
Unit tests for InterviewAgent
"""

import unittest
from unittest.mock import patch, MagicMock

from app.agents.interview_agent import InterviewAgent
from app.core.constants import AgentName


class TestInterviewAgent(unittest.TestCase):
    """Test cases for InterviewAgent"""

    def setUp(self):
        """Set up test fixtures"""
        self.agent = InterviewAgent()
        
        self.sample_input = {
            "resume_text": """
            John Doe
            Software Engineer with 3 years of experience in Python, Django, and AWS.
            Built REST APIs and microservices. Experience with PostgreSQL and Docker.
            """,
            "parsed_resume": {
                "personal_info": {"name": "John Doe"},
                "skills": ["Python", "Django", "AWS", "PostgreSQL", "Docker"],
                "experience": [{"title": "Software Engineer", "years": 3}]
            },
            "target_role": "Senior Python Developer",
            "experience_level": "Mid-level",
            "detected_skills": ["Python", "Django", "AWS", "PostgreSQL", "Docker"]
        }

    def test_init(self):
        """Test agent initialization"""
        self.assertEqual(self.agent.agent_name, AgentName.INTERVIEW)
        self.assertIsNotNone(self.agent._logger)

    @patch('app.agents.base_agent.BaseAgent._call_llm')
    @patch('app.agents.base_agent.BaseAgent._parse_json_response')
    def test_run_success(self, mock_parse_json, mock_call_llm):
        """Test successful interview question generation"""
        # Mock LLM response
        mock_call_llm.return_value = """
        {
            "technical_questions": [
                {
                    "question": "Explain Django ORM?",
                    "category": "technical",
                    "difficulty": "medium",
                    "hint": "Think about models and queries",
                    "why_asked": "Tests ORM knowledge",
                    "sample_answer": "Django ORM maps Python classes to database tables"
                }
            ],
            "coding_questions": [],
            "hr_questions": [],
            "project_questions": [],
            "conceptual_questions": [],
            "total_questions": 1,
            "difficulty_level": "medium",
            "preparation_tips": ["Practice Django concepts"]
        }
        """
        mock_parse_json.return_value = {
            "technical_questions": [
                {
                    "question": "Explain Django ORM?",
                    "category": "technical",
                    "difficulty": "medium",
                    "hint": "Think about models and queries",
                    "why_asked": "Tests ORM knowledge",
                    "sample_answer": "Django ORM maps Python classes to database tables"
                }
            ],
            "coding_questions": [],
            "hr_questions": [],
            "project_questions": [],
            "conceptual_questions": [],
            "total_questions": 1,
            "difficulty_level": "medium",
            "preparation_tips": ["Practice Django concepts"]
        }

        result = self.agent.run(self.sample_input)

        # Assertions
        self.assertTrue(result["success"])
        self.assertIsNone(result["error"])
        self.assertEqual(len(result["technical_questions"]), 1)
        self.assertEqual(result["technical_questions"][0]["question"], "Explain Django ORM?")
        self.assertEqual(result["total_questions"], 1)
        self.assertEqual(result["difficulty_level"], "medium")
        self.assertEqual(len(result["preparation_tips"]), 1)

    @patch('app.agents.base_agent.BaseAgent._call_llm')
    @patch('app.agents.base_agent.BaseAgent._parse_json_response')
    def test_run_empty_resume(self, mock_parse_json, mock_call_llm):
        """Test handling of empty resume text"""
        input_data = self.sample_input.copy()
        input_data["resume_text"] = ""

        result = self.agent.run(input_data)

        self.assertFalse(result["success"])
        self.assertEqual(result["error"], "No resume text provided.")
        self.assertEqual(result["technical_questions"], [])
        self.assertEqual(result["total_questions"], 0)

    @patch('app.agents.base_agent.BaseAgent._call_llm')
    @patch('app.agents.base_agent.BaseAgent._parse_json_response')
    def test_run_parse_failure(self, mock_parse_json, mock_call_llm):
        """Test handling of JSON parse failure"""
        mock_call_llm.return_value = "Invalid JSON response"
        mock_parse_json.return_value = {}

        result = self.agent.run(self.sample_input)

        self.assertFalse(result["success"])
        self.assertEqual(result["error"], "Could not parse interview questions.")
        self.assertEqual(result["technical_questions"], [])
        self.assertEqual(result["total_questions"], 0)

    @patch('app.agents.base_agent.BaseAgent._call_llm')
    def test_run_exception(self, mock_call_llm):
        """Test handling of unexpected exceptions"""
        mock_call_llm.side_effect = Exception("API error")

        result = self.agent.run(self.sample_input)

        self.assertFalse(result["success"])
        self.assertEqual(result["error"], "API error")
        self.assertEqual(result["technical_questions"], [])
        self.assertEqual(result["total_questions"], 0)


if __name__ == '__main__':
    unittest.main()