"""
TalentMind AI - Resume Repository
====================================
Database operations for Resume and Candidate models.
Implements Repository pattern for clean data access.

Author  : TalentMind AI Team
Version : 1.0.0
"""

from __future__ import annotations

import logging
from typing import Optional

from sqlalchemy.orm import Session

from app.core.exceptions import DatabaseError, RecordNotFoundError
from app.database.models import CandidateModel, ResumeModel

logger = logging.getLogger(__name__)


class ResumeRepository:
    """
    Handles all database operations for resumes
    and candidates.

    Why Repository Pattern:
        - Separates database logic from business logic
        - Makes testing easier with mock injection
        - Single place to change DB operations
        - Clean, readable service layer code
    """

    def __init__(self, session: Session) -> None:
        self._session = session

    def create_candidate(
        self,
        candidate_id : str,
        name         : Optional[str] = None,
        email        : Optional[str] = None,
        phone        : Optional[str] = None,
    ) -> CandidateModel:
        """
        Creates a new candidate record.

        Args:
            candidate_id : UUID string
            name         : Candidate full name
            email        : Email address
            phone        : Phone number

        Returns:
            CandidateModel: Created record
        """
        try:
            candidate = CandidateModel(
                id    = candidate_id,
                name  = name,
                email = email,
                phone = phone,
            )
            self._session.add(candidate)
            self._session.flush()

            logger.info(
                "Candidate created | id=%s | email=%s",
                candidate_id, email
            )
            return candidate

        except Exception as exc:
            logger.error(
                "Failed to create candidate | error=%s", exc
            )
            raise DatabaseError(
                f"Could not create candidate: {exc}"
            ) from exc

    def get_or_create_candidate(
        self,
        candidate_id : str,
        name         : Optional[str] = None,
        email        : Optional[str] = None,
    ) -> CandidateModel:
        """
        Returns existing candidate or creates new one.

        Args:
            candidate_id : UUID string
            name         : Optional name
            email        : Optional email

        Returns:
            CandidateModel: Existing or new candidate
        """
        candidate = self._session.get(
            CandidateModel, candidate_id
        )

        if candidate:
            logger.debug(
                "Candidate found | id=%s", candidate_id
            )
            return candidate

        return self.create_candidate(
            candidate_id=candidate_id,
            name=name,
            email=email,
        )

    def create_resume(
        self,
        resume_id    : str,
        candidate_id : str,
        file_name    : str,
        file_type    : str,
        raw_text     : str,
        parsed_data  : Optional[dict] = None,
    ) -> ResumeModel:
        """
        Creates a new resume record.

        Args:
            resume_id    : UUID from file processor
            candidate_id : Owner candidate ID
            file_name    : Sanitized filename
            file_type    : pdf / docx / txt
            raw_text     : Extracted text content
            parsed_data  : Optional parsed JSON data

        Returns:
            ResumeModel: Created record
        """
        try:
            resume = ResumeModel(
                id           = resume_id,
                candidate_id = candidate_id,
                file_name    = file_name,
                file_type    = file_type,
                raw_text     = raw_text,
                parsed_data  = parsed_data,
                is_active    = True,
            )
            self._session.add(resume)
            self._session.flush()

            logger.info(
                "Resume created | id=%s | file=%s",
                resume_id, file_name
            )
            return resume

        except Exception as exc:
            logger.error(
                "Failed to create resume | error=%s", exc
            )
            raise DatabaseError(
                f"Could not save resume: {exc}"
            ) from exc

    def get_resume_by_id(
        self,
        resume_id: str
    ) -> ResumeModel:
        """
        Retrieves resume by ID.

        Args:
            resume_id: Resume UUID

        Returns:
            ResumeModel: Found resume

        Raises:
            RecordNotFoundError: If not found
        """
        resume = self._session.get(ResumeModel, resume_id)

        if not resume:
            raise RecordNotFoundError(
                model="Resume",
                identifier=resume_id
            )

        return resume

    def get_latest_resume_for_candidate(
        self,
        candidate_id: str
    ) -> Optional[ResumeModel]:
        """
        Returns the most recent active resume.

        Args:
            candidate_id: Candidate UUID

        Returns:
            ResumeModel or None
        """
        resume = (
            self._session.query(ResumeModel)
            .filter(
                ResumeModel.candidate_id == candidate_id,
                ResumeModel.is_active    == True,
            )
            .order_by(ResumeModel.uploaded_at.desc())
            .first()
        )

        logger.debug(
            "Latest resume query | candidate=%s | found=%s",
            candidate_id, resume is not None
        )
        return resume

    def deactivate_previous_resumes(
        self,
        candidate_id  : str,
        keep_resume_id: str,
    ) -> int:
        """
        Deactivates all resumes except the specified one.
        Ensures only one active resume per candidate.

        Args:
            candidate_id   : Candidate UUID
            keep_resume_id : Resume to keep active

        Returns:
            int: Number of deactivated resumes
        """
        updated = (
            self._session.query(ResumeModel)
            .filter(
                ResumeModel.candidate_id == candidate_id,
                ResumeModel.id           != keep_resume_id,
                ResumeModel.is_active    == True,
            )
            .update({"is_active": False})
        )

        if updated > 0:
            logger.info(
                "Deactivated %d previous resumes | candidate=%s",
                updated, candidate_id
            )

        return updated