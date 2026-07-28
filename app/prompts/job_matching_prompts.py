"""
TalentMind AI - Job Matching Agent Prompts
==========================================
Author: TalentMind AI Team
Version: 1.0.0
"""

from __future__ import annotations

import string

JOB_MATCHING_PROMPT = string.Template("""You are an expert Job Matching AI.
Analyze the candidate's resume and match them to suitable job roles.

RESUME TEXT:
$resume_text

DETECTED SKILLS: $detected_skills
EXPERIENCE LEVEL: $experience_level
PRIMARY DOMAIN: $primary_domain
TARGET ROLE PREFERENCE: $target_role

Based on the candidate's profile, provide:
1. Top 5 job role matches with match percentages
2. Career progression paths for the top match
3. Internship recommendations (if candidate is a fresher/entry-level)
4. Industry fit analysis
5. Salary range estimates for the top match
6. Next role suggestion

Return a JSON object with EXACTLY this structure:
{
    "job_matches": [
        {
            "role": "Software Engineer",
            "match_score": 85,
            "match_label": "Strong Match",
            "required_skills": ["Python", "Django", "AWS"],
            "matching_skills": ["Python", "Django"],
            "missing_skills": ["AWS"],
            "why_good_fit": "Your Python experience aligns well...",
            "salary_range": "8-15 LPA",
            "companies": ["TCS", "Infosys", "Accenture"],
            "growth_path": "Junior → Mid → Senior → Lead"
        }
    ],
    "career_paths": [
        "Junior Developer → Senior Developer → Tech Lead → Architect",
        "Developer → Team Lead → Engineering Manager → Director"
    ],
    "internship_recs": [
        {
            "role": "Software Engineering Intern",
            "company": "Tech Company",
            "duration": "3 months",
            "stipend": "15000-25000 INR",
            "skills_to_learn": ["Python", "SQL", "Git"]
        }
    ],
    "industry_fit": [
        {
            "industry": "Information Technology",
            "fit_score": 85,
            "fit_description": "Strong fit due to strong programming skills"
        },
        {
            "industry": "Financial Technology",
            "fit_score": 75,
            "fit_description": "Good fit with fintech growth and demand for skilled developers"
        }
    ],
    "salary_range": {
        "min": 800000,
        "max": 1500000,
        "currency": "INR",
        "period": "per annum"
    },
    "next_role_suggestion": "Senior Software Engineer",
    "total_matches": 5
}

IMPORTANT:
- Return ONLY valid JSON
- Base matches on actual resume skills and experience
- Provide realistic salary ranges based on experience level and location (assume India if not specified)
- Explain why each role is a good fit
- For internships, only include if experience level is entry/fresher
- Career paths should show realistic progression
- Match labels: "Excellent Match" (85-100), "Good Match" (70-84), "Fair Match" (50-69), "Poor Match" (<50)
""")