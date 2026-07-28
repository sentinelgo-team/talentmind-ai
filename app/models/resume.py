"""
TalentMind AI - Resume Data Models
=====================================
Pydantic v2 compatible models for structured resume data.

Author  : TalentMind AI Team
Version : 1.0.0
"""

from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, field_serializer


class ContactInfo(BaseModel):
    """Candidate contact information."""
    name    : Optional[str] = Field(None, description="Full name")
    email   : Optional[str] = Field(None, description="Email address")
    phone   : Optional[str] = Field(None, description="Phone number")
    location: Optional[str] = Field(None, description="City, Country")
    linkedin: Optional[str] = Field(None, description="LinkedIn URL")
    github  : Optional[str] = Field(None, description="GitHub URL")
    website : Optional[str] = Field(None, description="Personal website")


class Education(BaseModel):
    """Single education record."""
    degree        : Optional[str] = Field(None)
    institution   : Optional[str] = Field(None)
    field_of_study: Optional[str] = Field(None)
    start_year    : Optional[str] = Field(None)
    end_year      : Optional[str] = Field(None)
    grade         : Optional[str] = Field(None)
    achievements  : List[str]     = Field(default_factory=list)


class WorkExperience(BaseModel):
    """Single work experience record."""
    job_title   : Optional[str] = Field(None)
    company     : Optional[str] = Field(None)
    location    : Optional[str] = Field(None)
    start_date  : Optional[str] = Field(None)
    end_date    : Optional[str] = Field(None)
    is_current  : bool          = Field(False)
    description : List[str]     = Field(default_factory=list)
    technologies: List[str]     = Field(default_factory=list)


class Project(BaseModel):
    """Single project record."""
    name        : Optional[str] = Field(None)
    description : Optional[str] = Field(None)
    technologies: List[str]     = Field(default_factory=list)
    role        : Optional[str] = Field(None)
    duration    : Optional[str] = Field(None)
    url         : Optional[str] = Field(None)
    highlights  : List[str]     = Field(default_factory=list)


class Certification(BaseModel):
    """Single certification record."""
    name         : Optional[str] = Field(None)
    issuer       : Optional[str] = Field(None)
    date         : Optional[str] = Field(None)
    expiry       : Optional[str] = Field(None)
    credential_id: Optional[str] = Field(None)
    url          : Optional[str] = Field(None)


class ParsedResume(BaseModel):
    """
    Complete structured resume data.
    Output model of the Resume Agent.
    Pydantic v2 compatible.
    """
    contact_info          : ContactInfo          = Field(
        default_factory=ContactInfo
    )
    summary               : Optional[str]        = Field(None)
    education             : List[Education]      = Field(
        default_factory=list
    )
    experience            : List[WorkExperience] = Field(
        default_factory=list
    )
    projects              : List[Project]        = Field(
        default_factory=list
    )
    certifications        : List[Certification]  = Field(
        default_factory=list
    )
    skills                : List[str]            = Field(
        default_factory=list
    )
    languages             : List[str]            = Field(
        default_factory=list
    )
    total_experience_years: float                = Field(0.0)
    parsed_at             : datetime             = Field(
        default_factory=datetime.now
    )

    # ── Pydantic v2 datetime serializer ──────────────────────
    @field_serializer("parsed_at")
    def serialize_datetime(self, value: datetime) -> str:
        """Serializes datetime to ISO format string."""
        return value.isoformat()