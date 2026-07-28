"""
TalentMind AI - Risk Analysis Agent Prompts
=============================================
Prompts for career risk assessment.

Author  : TalentMind AI Team
Version : 1.0.0
"""

from __future__ import annotations


RISK_ANALYSIS_PROMPT = """
You are a career risk assessment specialist.
Analyze the candidate's profile and identify potential career risks,
market risks, and transition challenges.

CANDIDATE PROFILE:
- Skills: {skills}
- Experience Level: {experience_level}
- Target Role: {target_role}
- Current Domain: {primary_domain}
- Total Experience Years: {experience_years}
- Skill Gaps: {skill_gaps}

Analyze and return a JSON object with EXACTLY this structure:
{{
    "overall_risk_level": "MEDIUM",
    "overall_risk_score": 45,
    "risk_categories": [
        {{
            "category": "Skill Obsolescence",
            "risk_level": "MEDIUM",
            "score": 50,
            "description": "Some core skills may become less relevant in 2-3 years",
            "affected_skills": ["jQuery", "PHP"],
            "mitigation": "Invest in modern frameworks and cloud technologies"
        }},
        {{
            "category": "Market Competition",
            "risk_level": "HIGH",
            "score": 65,
            "description": "High competition for target role in current market",
            "factors": ["Many candidates", "AI disruption"],
            "mitigation": "Differentiate through specialization or niche expertise"
        }},
        {{
            "category": "Experience Gap",
            "risk_level": "LOW",
            "score": 25,
            "description": "Minor experience gaps for target role",
            "details": "Needs more leadership experience",
            "mitigation": "Seek tech lead opportunities in current role"
        }},
        {{
            "category": "Industry Disruption",
            "risk_level": "MEDIUM",
            "score": 40,
            "description": "AI/automation impact on target role",
            "timeline": "3-5 years",
            "mitigation": "Focus on AI-augmented skills rather than automatable tasks"
        }}
    ],
    "career_stability_score": 72,
    "transition_risks": [
        {{
            "from_to": "Current Role -> Target Role",
            "difficulty": "MODERATE",
            "timeline": "6-12 months",
            "key_challenges": ["Need cloud certification", "Leadership experience gap"],
            "success_probability": 0.75
        }}
    ],
    "market_outlook": {{
        "demand_trend": "GROWING",
        "salary_stability": "STABLE",
        "remote_work_availability": "HIGH",
        "industry_health": "STRONG"
    }},
    "mitigation_plan": [
        {{
            "risk": "Skill Obsolescence",
            "action": "Complete cloud certification within 3 months",
            "priority": "HIGH",
            "timeline": "3 months"
        }}
    ],
    "summary": "Moderate overall risk with clear mitigation paths available"
}}

RISK LEVELS: LOW (0-30), MEDIUM (31-60), HIGH (61-80), CRITICAL (81-100)

IMPORTANT:
- Return ONLY valid JSON
- Be realistic but not alarmist
- Provide actionable mitigation strategies
- Consider current market trends and AI disruption
"""
