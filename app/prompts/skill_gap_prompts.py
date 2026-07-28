"""
TalentMind AI - Skill Gap Analysis Prompts
============================================
Purpose: LLM prompt templates for skill gap detection,
         learning roadmap generation, and industry comparison.

Author  : TalentMind AI Team
Version : 1.0.0
"""

from __future__ import annotations


# ══════════════════════════════════════════════════════════════════
# SKILL GAP ANALYSIS PROMPT
# ══════════════════════════════════════════════════════════════════

SKILL_GAP_ANALYSIS_PROMPT = """
You are a Senior Technical Recruiter and Career Coach with 15+ years
of experience helping engineers bridge skill gaps.

Analyze the following candidate profile against industry requirements
and identify specific skill gaps with actionable recommendations.

CANDIDATE PROFILE:
Current Skills: {current_skills}
Experience Level: {experience_level}
Primary Domain: {primary_domain}

TARGET ROLE: {target_role}

INDUSTRY REQUIREMENTS FOR THIS ROLE:
Must Have: {must_have_skills}
Good to Have: {good_to_have_skills}
Bonus Skills: {bonus_skills}

YOUR TASK:
1. Compare candidate skills against requirements
2. Identify each missing skill with priority level
3. Explain WHY each skill is important for the role
4. Suggest learning approach for each gap
5. Provide overall readiness assessment

OUTPUT FORMAT (strict JSON only, no markdown):
{{
    "overall_readiness_score": 65,
    "readiness_label": "Partially Ready",
    "skill_gaps": [
        {{
            "skill": "Docker",
            "priority": "critical",
            "reason": "Required for all modern deployments",
            "current_level": "none",
            "target_level": "intermediate",
            "learning_suggestion": "Complete Docker official tutorial + build 2 projects",
            "estimated_weeks": 3
        }}
    ],
    "matched_skills": [
        {{
            "skill": "Python",
            "proficiency_match": "excellent",
            "comment": "Exceeds requirements"
        }}
    ],
    "critical_gaps_count": 3,
    "high_gaps_count": 2,
    "medium_gaps_count": 4,
    "low_gaps_count": 1,
    "strengths": [
        "Strong Python foundation",
        "Good database knowledge"
    ],
    "improvement_areas": [
        "Cloud platform experience needed",
        "DevOps skills required"
    ],
    "career_advice": "Focus on cloud and DevOps to become job-ready in 3 months",
    "industry_insight": "Python developers with Docker/K8s knowledge are in high demand"
}}

PRIORITY LEVELS (use exactly):
- "critical" : Must have to even apply for the role
- "high"     : Significantly improves interview chances
- "medium"   : Good to have, makes you more competitive
- "low"      : Nice to have, long-term career enhancement

READINESS LABELS (use exactly):
- "Not Ready"         : score < 40
- "Partially Ready"   : score 40-60
- "Mostly Ready"      : score 61-80
- "Ready"             : score > 80

Return ONLY valid JSON. No explanations outside JSON.
"""


# ══════════════════════════════════════════════════════════════════
# LEARNING ROADMAP GENERATION PROMPT
# ══════════════════════════════════════════════════════════════════

LEARNING_ROADMAP_PROMPT = """
You are an expert Career Development Coach and Technical Mentor.

Create a detailed, actionable learning roadmap for the following
candidate to close their skill gaps and achieve career goals.

CANDIDATE DETAILS:
Experience Level  : {experience_level}
Target Role       : {target_role}
Current Skills    : {current_skills}
Skill Gaps        : {skill_gaps}
Readiness Score   : {readiness_score}

YOUR TASK:
Create a structured learning roadmap with specific resources,
timelines, and milestones.

OUTPUT FORMAT (strict JSON only, no markdown):
{{
    "roadmap_title": "Path to Senior Python Developer",
    "total_duration_weeks": 16,
    "learning_phases": [
        {{
            "phase": 1,
            "name": "Foundation Building",
            "duration_weeks": 4,
            "focus": "Critical skill gaps",
            "skills_to_learn": [
                {{
                    "skill": "Docker",
                    "resources": [
                        "Docker Official Documentation",
                        "Docker & Kubernetes Udemy Course"
                    ],
                    "daily_time_hours": 1.5,
                    "project": "Containerize your existing Python app",
                    "success_criteria": "Deploy app in Docker container"
                }}
            ]
        }}
    ],
    "weekly_schedule": [
        {{
            "week": 1,
            "focus_skill": "Docker Basics",
            "daily_tasks": [
                "Complete Docker getting started tutorial",
                "Practice docker run commands",
                "Build first Dockerfile"
            ],
            "weekend_project": "Containerize a simple Flask app"
        }}
    ],
    "certifications_recommended": [
        {{
            "name": "AWS Certified Developer Associate",
            "provider": "Amazon",
            "timeline": "Month 3",
            "benefit": "Validates cloud skills for employers"
        }}
    ],
    "portfolio_projects": [
        {{
            "project": "Microservices with Docker",
            "skills_demonstrated": ["Docker", "Python", "PostgreSQL"],
            "estimated_days": 7,
            "github_worthy": true
        }}
    ],
    "success_metrics": [
        "Complete 3 Docker projects by week 4",
        "Deploy app to AWS by week 8",
        "Complete 2 certifications by month 4"
    ]
}}

Return ONLY valid JSON. No explanations outside JSON.
"""