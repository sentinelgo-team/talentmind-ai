"""
TalentMind AI - Integration Tests: Memory Manager
===================================================
Tests for the MemoryManager CRUD operations.

Author  : TalentMind AI Team
Version : 1.0.0
"""

from __future__ import annotations

import unittest
import uuid

from app.memory.memory_manager import MemoryManager, VALID_MEMORY_TYPES
from app.database.connection import db_manager
from app.database.models import CandidateModel


class TestMemoryManager(unittest.TestCase):
    """Tests for MemoryManager CRUD operations."""

    @classmethod
    def setUpClass(cls):
        """Initialize database tables."""
        db_manager.create_tables()

    def setUp(self):
        self.manager = MemoryManager()
        self.candidate_id = str(uuid.uuid4())
        # Create a candidate record to satisfy FK constraint
        with db_manager.get_session() as session:
            candidate = CandidateModel(
                id=self.candidate_id,
                name="Test Candidate",
            )
            session.add(candidate)

    def tearDown(self):
        """Clean up test data."""
        try:
            self.manager.delete_candidate_memories(
                self.candidate_id
            )
        except Exception:
            pass
        try:
            with db_manager.get_session() as session:
                session.query(CandidateModel).filter(
                    CandidateModel.id == self.candidate_id
                ).delete()
        except Exception:
            pass

    def test_valid_memory_types(self):
        """Test that valid memory types are defined."""
        self.assertIn("resume_analysis", VALID_MEMORY_TYPES)
        self.assertIn("ats_analysis", VALID_MEMORY_TYPES)
        self.assertIn("skill_analysis", VALID_MEMORY_TYPES)
        self.assertEqual(len(VALID_MEMORY_TYPES), 8)

    def test_store_and_retrieve_memory(self):
        """Test storing and retrieving a memory."""
        content = {"score": 85, "summary": "Good candidate"}

        memory_id = self.manager.store_memory(
            candidate_id=self.candidate_id,
            memory_type="resume_analysis",
            content=content,
            store_embedding=False,
        )

        self.assertIsNotNone(memory_id)

        result = self.manager.get_memory(
            candidate_id=self.candidate_id,
            memory_type="resume_analysis",
        )

        self.assertEqual(result["content"]["score"], 85)
        self.assertEqual(result["memory_type"], "resume_analysis")

    def test_upsert_behavior(self):
        """Test that store_memory updates existing records."""
        content_v1 = {"version": 1}
        content_v2 = {"version": 2}

        id1 = self.manager.store_memory(
            candidate_id=self.candidate_id,
            memory_type="ats_analysis",
            content=content_v1,
            store_embedding=False,
        )

        id2 = self.manager.store_memory(
            candidate_id=self.candidate_id,
            memory_type="ats_analysis",
            content=content_v2,
            store_embedding=False,
        )

        # Should update same record
        self.assertEqual(id1, id2)

        result = self.manager.get_memory(
            candidate_id=self.candidate_id,
            memory_type="ats_analysis",
        )
        self.assertEqual(result["content"]["version"], 2)

    def test_get_all_memories(self):
        """Test retrieving all memories for a candidate."""
        self.manager.store_memory(
            candidate_id=self.candidate_id,
            memory_type="resume_analysis",
            content={"type": "resume"},
            store_embedding=False,
        )
        self.manager.store_memory(
            candidate_id=self.candidate_id,
            memory_type="skill_analysis",
            content={"type": "skill"},
            store_embedding=False,
        )

        all_memories = self.manager.get_all_memories(
            self.candidate_id
        )
        self.assertEqual(len(all_memories), 2)

    def test_delete_memory(self):
        """Test deleting a single memory."""
        memory_id = self.manager.store_memory(
            candidate_id=self.candidate_id,
            memory_type="job_match",
            content={"test": True},
            store_embedding=False,
        )

        self.manager.delete_memory(memory_id)

        from app.core.exceptions import RecordNotFoundError
        with self.assertRaises(RecordNotFoundError):
            self.manager.get_memory(
                self.candidate_id, "job_match"
            )

    def test_invalid_memory_type_raises(self):
        """Test that invalid memory types raise ValueError."""
        with self.assertRaises(ValueError):
            self.manager.store_memory(
                candidate_id=self.candidate_id,
                memory_type="invalid_type",
                content={},
            )

    def test_delete_candidate_memories(self):
        """Test bulk deletion of candidate memories."""
        self.manager.store_memory(
            candidate_id=self.candidate_id,
            memory_type="resume_analysis",
            content={"a": 1},
            store_embedding=False,
        )
        self.manager.store_memory(
            candidate_id=self.candidate_id,
            memory_type="skill_analysis",
            content={"b": 2},
            store_embedding=False,
        )

        count = self.manager.delete_candidate_memories(
            self.candidate_id
        )
        self.assertEqual(count, 2)

        remaining = self.manager.get_all_memories(
            self.candidate_id
        )
        self.assertEqual(len(remaining), 0)


if __name__ == "__main__":
    unittest.main()
