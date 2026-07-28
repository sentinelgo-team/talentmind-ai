"""
TalentMind AI - Resume Agent Prompts
=======================================
All prompts used by the Resume Parsing Agent.
Centralized for easy maintenance and versioning.

Author  : TalentMind AI Team
Version : 1.0.0
"""

from __future__ import annotations


RESUME_PARSING_PROMPT = """
You are an expert Resume Parser AI.
Your task is to extract structured information from the resume text below.

RESUME TEXT:
{resume_text}

Extract and return a JSON object with EXACTLY this structure:
{{
    "contact_info": {{
        "name"      : "Full name or null",
        "email"     : "Email or null",
        "phone"     : "Phone or null",
        "location"  : "City, Country or null",
        "linkedin"  : "LinkedIn URL or null",
        "github"    : "GitHub URL or null",
        "website"   : "Website URL or null"
    }},
    "summary": "Professional summary text or null",
    "education": [
        {{
            "degree"        : "Degree name",
            "institution"   : "University name",
            "field_of_study": "Major/specialization",
            "start_year"    : "YYYY or null",
            "end_year"      : "YYYY or Present",
            "grade"         : "GPA/percentage or null",
            "achievements"  : ["achievement 1", "achievement 2"]
        }}
    ],
    "experience": [
        {{
            "job_title"   : "Job title",
            "company"     : "Company name",
            "location"    : "Location or null",
            "start_date"  : "Month YYYY or null",
            "end_date"    : "Month YYYY or Present",
            "is_current"  : false,
            "description" : ["responsibility 1", "responsibility 2"],
            "technologies": ["tech1", "tech2"]
        }}
    ],
    "projects": [
        {{
            "name"        : "Project name",
            "description" : "What the project does",
            "technologies": ["tech1", "tech2"],
            "role"        : "Your role",
            "duration"    : "Duration or null",
            "url"         : "URL or null",
            "highlights"  : ["highlight 1", "highlight 2"]
        }}
    ],
    "certifications": [
        {{
            "name"         : "Certification name",
            "issuer"       : "Issuing org",
            "date"         : "Date or null",
            "expiry"       : "Expiry or null",
            "credential_id": "ID or null",
            "url"          : "URL or null"
        }}
    ],
    "skills"    : ["skill1", "skill2", "skill3"],
    "languages" : ["English", "Hindi"],
    "total_experience_years": 0.0
}}

IMPORTANT RULES:
1. Return ONLY valid JSON - no extra text
2. Use null for missing values
3. Extract ALL skills mentioned anywhere
4. Calculate total_experience_years from work history
5. Keep descriptions as bullet point arrays
6. Include technologies from projects in skills
"""


RESUME_SUMMARY_PROMPT = """
Based on this parsed resume data, provide a brief
professional assessment in 2-3 sentences.

Candidate: {name}
Skills: {skills}
Experience: {experience_years} years
Education: {education}

Assessment:
"""