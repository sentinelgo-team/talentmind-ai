"""
TalentMind AI - Ranking Agent Prompts
=======================================
Prompts for candidate ranking and scoring.

Author  : TalentMind AI Team
Version : 1.0.0
"""

from __future__ import annotations


RANKING_PROMPT = """
You are an expert talent evaluator and recruitment specialist.
Evaluate the candidate's overall profile and provide a comprehensive ranking assessment.

CANDIDATE PROFILE:
- Resume Text (excerpt): {resume_text}
- Target Role: {target_role}
- Experience Level: {experience_level}
- Skills Count: {skills_count}
- ATS Score: {ats_score}

ANALYSIS RESULTS:
- Skill Match Percentage: {skill_match_pct}
- Critical Gaps: {critical_gaps}
- Strengths: {strengths}

Analyze and return a JSON object with EXACTLY this structure:
{{
    "overall_rank_score": 78,
    "rank_label": "Strong Candidate",
    "dimension_scores": {{
        "technical_proficiency": 82,
        "experience_relevance": 75,
        "education_quality": 80,
        "project_impact": 70,
        "communication_skills": 85,
        "leadership_potential": 65,
        "cultural_fit_indicators": 78,
        "growth_potential": 88
    }},
    "competitive_position": {{
        "percentile": 72,
        "market_position": "Above Average",
        "differentiators": ["Strong open-source contributions", "Cross-functional experience"],
        "areas_below_peers": ["Limited leadership experience", "No cloud certifications"]
    }},
    "hiring_recommendation": {{
        "decision": "RECOMMEND",
        "confidence": 0.78,
        "reasoning": "Strong technical skills with clear growth trajectory",
        "ideal_roles": ["Senior Engineer", "Tech Lead (with mentoring)"],
        "concerns": ["May need 6 months to ramp up on cloud infrastructure"]
    }},
    "improvement_impact": [
        {{
            "action": "Obtain cloud certification",
            "score_improvement": 8,
            "new_rank": "Top Candidate"
        }}
    ]
}}

SCORING RULES:
- overall_rank_score: 0-100
- dimension_scores: Each 0-100
- percentile: Where candidate falls among similar applicants
- decision: STRONGLY_RECOMMEND / RECOMMEND / CONSIDER / NOT_RECOMMENDED

IMPORTANT:
- Return ONLY valid JSON
- Be objective and evidence-based
- Score based on the actual content provided
"""
