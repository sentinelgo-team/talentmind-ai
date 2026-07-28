"""
TalentMind AI - SQLAlchemy ORM Models
=======================================
Database table definitions with proper relationships,
constraints, and indexing for optimal performance.

Author  : TalentMind AI Team
Version : 1.0.0
"""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from sqlalchemy import (
    Boolean, DateTime, Float, ForeignKey,
    Index, Integer, JSON, String, Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.connection import Base


def generate_uuid() -> str:
    """Generates a new UUID string."""
    return str(uuid.uuid4())


# ── Candidate Model ──────────────────────────────────────────
class CandidateModel(Base):
    """
    Represents a candidate in the system.
    Central entity linked to resumes and analyses.
    """
    __tablename__ = "candidates"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True,
        default=generate_uuid
    )
    name: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True
    )
    email: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True, unique=True, index=True
    )
    phone: Mapped[Optional[str]] = mapped_column(
        String(20), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(),
        onupdate=func.now(), nullable=False
    )

    # Relationships
    resumes: Mapped[List["ResumeModel"]] = relationship(
        "ResumeModel", back_populates="candidate",
        cascade="all, delete-orphan"
    )
    reports: Mapped[List["ReportModel"]] = relationship(
        "ReportModel", back_populates="candidate",
        cascade="all, delete-orphan"
    )
    memories: Mapped[List["MemoryModel"]] = relationship(
        "MemoryModel", back_populates="candidate",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"CandidateModel(id={self.id!r}, email={self.email!r})"


# ── Resume Model ─────────────────────────────────────────────
class ResumeModel(Base):
    """
    Stores uploaded resume data and extracted text.
    """
    __tablename__ = "resumes"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True,
        default=generate_uuid
    )
    candidate_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("candidates.id", ondelete="CASCADE"),
        nullable=False, index=True
    )
    file_name: Mapped[str] = mapped_column(
        String(255), nullable=False
    )
    file_type: Mapped[str] = mapped_column(
        String(10), nullable=False
    )
    raw_text: Mapped[Optional[str]] = mapped_column(
        Text, nullable=True
    )
    parsed_data: Mapped[Optional[Dict]] = mapped_column(
        JSON, nullable=True
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False
    )
    uploaded_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), nullable=False
    )

    # Relationships
    candidate: Mapped["CandidateModel"] = relationship(
        "CandidateModel", back_populates="resumes"
    )
    analyses: Mapped[List["AnalysisModel"]] = relationship(
        "AnalysisModel", back_populates="resume",
        cascade="all, delete-orphan"
    )
    ats_results: Mapped[List["ATSResultModel"]] = relationship(
        "ATSResultModel", back_populates="resume",
        cascade="all, delete-orphan"
    )
    skill_analyses: Mapped[List["SkillAnalysisModel"]] = relationship(
        "SkillAnalysisModel", back_populates="resume",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return (
            f"ResumeModel(id={self.id!r}, "
            f"file={self.file_name!r})"
        )


# ── Analysis Model ───────────────────────────────────────────
class AnalysisModel(Base):
    """
    Generic analysis result store for all agent outputs.
    """
    __tablename__ = "analyses"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True,
        default=generate_uuid
    )
    resume_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("resumes.id", ondelete="CASCADE"),
        nullable=False, index=True
    )
    analysis_type: Mapped[str] = mapped_column(
        String(50), nullable=False, index=True
    )
    result_data: Mapped[Optional[Dict]] = mapped_column(
        JSON, nullable=True
    )
    score: Mapped[Optional[float]] = mapped_column(
        Float, nullable=True
    )
    agent_version: Mapped[str] = mapped_column(
        String(20), default="1.0.0", nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), nullable=False
    )

    # Relationships
    resume: Mapped["ResumeModel"] = relationship(
        "ResumeModel", back_populates="analyses"
    )

    # Indexes
    __table_args__ = (
        Index(
            "ix_analyses_resume_type",
            "resume_id", "analysis_type"
        ),
    )


# ── ATS Result Model ─────────────────────────────────────────
class ATSResultModel(Base):
    """Stores ATS compatibility analysis results."""

    __tablename__ = "ats_results"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=generate_uuid
    )
    resume_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("resumes.id", ondelete="CASCADE"),
        nullable=False, index=True
    )
    overall_score: Mapped[float] = mapped_column(
        Float, nullable=False
    )
    keyword_score: Mapped[float] = mapped_column(
        Float, nullable=False
    )
    format_score: Mapped[float] = mapped_column(
        Float, nullable=False
    )
    grammar_score: Mapped[float] = mapped_column(
        Float, nullable=False
    )
    suggestions: Mapped[Optional[Dict]] = mapped_column(
        JSON, nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), nullable=False
    )

    resume: Mapped["ResumeModel"] = relationship(
        "ResumeModel", back_populates="ats_results"
    )


# ── Skill Analysis Model ─────────────────────────────────────
class SkillAnalysisModel(Base):
    """Stores skill detection and gap analysis results."""

    __tablename__ = "skill_analyses"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=generate_uuid
    )
    resume_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("resumes.id", ondelete="CASCADE"),
        nullable=False, index=True
    )
    detected_skills: Mapped[Optional[Dict]] = mapped_column(
        JSON, nullable=True
    )
    missing_skills: Mapped[Optional[Dict]] = mapped_column(
        JSON, nullable=True
    )
    skill_scores: Mapped[Optional[Dict]] = mapped_column(
        JSON, nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), nullable=False
    )

    resume: Mapped["ResumeModel"] = relationship(
        "ResumeModel", back_populates="skill_analyses"
    )


# ── Report Model ─────────────────────────────────────────────
class ReportModel(Base):
    """Stores generated PDF report metadata."""

    __tablename__ = "reports"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=generate_uuid
    )
    candidate_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("candidates.id", ondelete="CASCADE"),
        nullable=False, index=True
    )
    resume_id: Mapped[Optional[str]] = mapped_column(
        String(36), nullable=True
    )
    report_path: Mapped[str] = mapped_column(
        String(500), nullable=False
    )
    report_type: Mapped[str] = mapped_column(
        String(50), default="full_report", nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), nullable=False
    )

    candidate: Mapped["CandidateModel"] = relationship(
        "CandidateModel", back_populates="reports"
    )


# ── Memory Model ─────────────────────────────────────────────
class MemoryModel(Base):
    """Stores agent memory and conversation history."""

    __tablename__ = "memory_store"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=generate_uuid
    )
    candidate_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("candidates.id", ondelete="CASCADE"),
        nullable=False, index=True
    )
    memory_type: Mapped[str] = mapped_column(
        String(50), nullable=False, index=True
    )
    content: Mapped[Optional[Dict]] = mapped_column(
        JSON, nullable=True
    )
    embedding_id: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), nullable=False
    )

    candidate: Mapped["CandidateModel"] = relationship(
        "CandidateModel", back_populates="memories"
    )