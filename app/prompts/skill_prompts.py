"""
TalentMind AI - Skill Agent Prompts
======================================
Author  : TalentMind AI Team
Version : 1.0.0
"""

from __future__ import annotations


SKILL_ANALYSIS_PROMPT = """
You are an expert Technical Skill Analyzer AI.
Analyze the resume below and provide a comprehensive skill analysis.

RESUME TEXT:
{resume_text}

TARGET ROLE: {target_role}

Return a JSON object with EXACTLY this structure:
{{
    "detected_skills": [
        {{
            "name"       : "Python",
            "category"   : "Programming Languages",
            "proficiency": "Intermediate",
            "evidence"   : "Used in multiple projects",
            "score"      : 70
        }}
    ],
    "skill_categories": {{
        "Programming Languages" : ["Python", "Go"],
        "Security Tools"        : ["Burp Suite", "Nmap"],
        "Operating Systems"     : ["Linux", "Windows"],
        "Frameworks"            : [],
        "Cloud & DevOps"        : [],
        "Databases"             : [],
        "Soft Skills"           : [],
        "Other"                 : []
    }},
    "proficiency_summary": {{
        "Expert"      : [],
        "Advanced"    : [],
        "Intermediate": ["Python", "Go"],
        "Beginner"    : []
    }},
    "industry_comparison": {{
        "role"               : "Cybersecurity Analyst",
        "required_skills"    : ["Python", "SIEM", "Wireshark"],
        "candidate_has"      : ["Python", "Linux"],
        "candidate_missing"  : ["SIEM", "Wireshark"],
        "match_percentage"   : 65,
        "comparison_comment" : "Strong foundation but missing enterprise tools"
    }},
    "skill_scores": {{
        "technical_score"  : 72,
        "diversity_score"  : 65,
        "relevance_score"  : 78,
        "overall_score"    : 72
    }},
    "top_skills"    : ["Python", "Linux", "Go"],
    "skill_gaps"    : ["SIEM", "Wireshark", "Docker"],
    "recommendations": [
        "Learn Wireshark for network analysis",
        "Study SIEM tools like Splunk"
    ],
    "total_skills_count": 17
}}

PROFICIENCY LEVELS:
- Expert       : 5+ years, deep knowledge
- Advanced     : 3-5 years, strong practical use
- Intermediate : 1-3 years, regular use
- Beginner     : < 1 year, basic knowledge

IMPORTANT:
- Return ONLY valid JSON
- Categorize ALL skills found in resume
- Be realistic about proficiency levels
- Base industry comparison on target role
"""