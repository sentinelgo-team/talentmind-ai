"""
TalentMind AI - Application Constants
=======================================
Centralized constants used across the application.
Never hardcode these values in business logic.

Author  : TalentMind AI Team
Version : 1.0.0
"""

from __future__ import annotations
from typing import Dict, List, FrozenSet


# ── Application Info ─────────────────────────────────────────
APP_NAME         = "TalentMind AI"
APP_TAGLINE      = "Intelligent Recruitment & Career Guidance"
APP_VERSION      = "1.0.0"
APP_AUTHOR       = "TalentMind AI Team"


# ── File Processing ──────────────────────────────────────────
SUPPORTED_FILE_TYPES: FrozenSet[str] = frozenset({
    "pdf", "docx", "txt"
})
MAX_FILE_SIZE_MB         = 10
MIN_RESUME_TEXT_LENGTH   = 100   # chars
MAX_RESUME_TEXT_LENGTH   = 50_000  # chars


# ── Agent Names ──────────────────────────────────────────────
class AgentName:
    """Agent identifier constants."""
    RESUME         = "ResumeAgent"
    ATS            = "ATSAgent"
    SKILL          = "SkillAnalysisAgent"
    JOB_MATCHING   = "JobMatchingAgent"
    SKILL_GAP      = "SkillGapAgent"
    INTERVIEW      = "InterviewAgent"
    RANKING        = "RankingAgent"
    RECOMMENDATION = "RecommendationAgent"
    REFLECTION     = "ReflectionAgent"
    RISK           = "RiskAnalysisAgent"
    MEMORY         = "MemoryAgent"
    PDF_REPORT     = "PDFReportAgent"
    DASHBOARD      = "DashboardAgent"
    ROUTER         = "LangGraphRouterAgent"


# ── Score Ranges ─────────────────────────────────────────────
class ScoreRange:
    """Score boundary constants."""
    MIN              = 0
    MAX              = 100
    EXCELLENT_MIN    = 85
    GOOD_MIN         = 70
    AVERAGE_MIN      = 50
    POOR_MAX         = 49


# ── Score Labels ─────────────────────────────────────────────
SCORE_LABELS: Dict[str, str] = {
    "excellent" : "Excellent",
    "good"      : "Good",
    "average"   : "Average",
    "poor"      : "Needs Improvement",
}


# ── Risk Levels ──────────────────────────────────────────────
class RiskLevel:
    """Risk classification constants."""
    LOW      = "LOW"
    MEDIUM   = "MEDIUM"
    HIGH     = "HIGH"
    CRITICAL = "CRITICAL"


# ── Analysis Types ───────────────────────────────────────────
class AnalysisType:
    """Database analysis type identifiers."""
    RESUME         = "resume_analysis"
    ATS            = "ats_analysis"
    SKILL          = "skill_analysis"
    JOB_MATCH      = "job_match"
    SKILL_GAP      = "skill_gap"
    INTERVIEW      = "interview_prep"
    RANKING        = "candidate_ranking"
    RECOMMENDATION = "recommendations"
    RISK           = "risk_analysis"


# ── Skill Categories ─────────────────────────────────────────
SKILL_CATEGORIES: List[str] = [
    "Programming Languages",
    "Web Development",
    "Mobile Development",
    "Data Science & ML",
    "Cloud & DevOps",
    "Databases",
    "Frameworks & Libraries",
    "Tools & Platforms",
    "Soft Skills",
    "Domain Knowledge",
]


# ── Job Categories ───────────────────────────────────────────
JOB_CATEGORIES: List[str] = [
    "Software Development",
    "Data Science & Analytics",
    "Machine Learning & AI",
    "DevOps & Cloud",
    "UI/UX Design",
    "Product Management",
    "Cybersecurity",
    "Database Administration",
    "Mobile Development",
    "Business Analysis",
]


# ── Interview Question Types ─────────────────────────────────
class InterviewQuestionType:
    """Interview question category constants."""
    TECHNICAL    = "technical"
    CODING       = "coding"
    HR           = "hr"
    BEHAVIORAL   = "behavioral"
    PROJECT      = "project"
    SITUATIONAL  = "situational"


# ── UI Constants ─────────────────────────────────────────────
class UIColor:
    """Brand color constants for UI."""
    PRIMARY      = "#2563EB"
    SECONDARY    = "#7C3AED"
    SUCCESS      = "#059669"
    WARNING      = "#D97706"
    DANGER       = "#DC2626"
    INFO         = "#0891B2"
    BACKGROUND   = "#F8FAFC"
    CARD         = "#FFFFFF"
    TEXT         = "#1E293B"
    MUTED        = "#64748B"


# ── Status Constants ─────────────────────────────────────────
class ProcessingStatus:
    """Processing state constants."""
    PENDING    = "pending"
    PROCESSING = "processing"
    COMPLETED  = "completed"
    FAILED     = "failed"
    CANCELLED  = "cancelled"


# ── Error Codes ──────────────────────────────────────────────
class ErrorCode:
    """Application error code constants."""
    GENERIC           = "ERR_GENERIC"
    FILE_TYPE         = "ERR_FILE_TYPE"
    FILE_SIZE         = "ERR_FILE_SIZE"
    EXTRACTION        = "ERR_EXTRACTION"
    API_KEY           = "ERR_API_KEY"
    AGENT_FAILURE     = "ERR_AGENT"
    DATABASE          = "ERR_DATABASE"
    VALIDATION        = "ERR_VALIDATION"
    NOT_FOUND         = "ERR_NOT_FOUND"