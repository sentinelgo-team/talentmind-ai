"""
TalentMind AI - Memory Manager
================================
Manages persistent storage and retrieval of analysis results
per candidate, with optional FAISS-based semantic search.

Author  : TalentMind AI Team
Version : 1.0.0
"""

from __future__ import annotations

import json
import logging
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import numpy as np

from app.core.exceptions import (
    DatabaseError,
    RecordNotFoundError,
)
from app.core.settings import get_settings
from app.database.connection import db_manager
from app.database.models import MemoryModel

logger = logging.getLogger(__name__)
cfg = get_settings()


# ── Valid Memory Types ───────────────────────────────────────
VALID_MEMORY_TYPES = frozenset({
    "resume_analysis",
    "ats_analysis",
    "skill_analysis",
    "skill_gap",
    "job_match",
    "interview_prep",
    "recommendations",
    "risk_analysis",
})


class MemoryManager:
    """
    Manages candidate analysis memory with persistent storage
    and optional vector-based semantic search.

    Features:
        - CRUD operations for candidate memories
        - Keyed storage by candidate_id + memory_type
        - FAISS vector index for semantic similarity search
        - Graceful degradation when embeddings unavailable
        - Consistent error handling with project exceptions

    Example:
        from app.memory import MemoryManager

        memory = MemoryManager()
        memory.store_memory(
            candidate_id="abc-123",
            memory_type="resume_analysis",
            content={"score": 85, "summary": "Strong backend dev"}
        )
    """

    _faiss_index: Any = None
    _embedding_map: Dict[str, int] = {}
    _index_initialized: bool = False

    def __init__(self) -> None:
        """Initializes MemoryManager with optional FAISS index."""
        self._logger = logging.getLogger("memory.manager")
        self._vector_dir = cfg.vector_db_dir_path
        self._embeddings_enabled = self._init_vector_store()

    # ── CRUD Operations ──────────────────────────────────────

    def store_memory(
        self,
        candidate_id: str,
        memory_type: str,
        content: Dict[str, Any],
        *,
        store_embedding: bool = True,
    ) -> str:
        """
        Stores a memory record for a candidate.

        If a memory with the same candidate_id and memory_type
        already exists, it will be updated (upsert behavior).

        Args:
            candidate_id   : UUID of the candidate
            memory_type    : Type of analysis result
            content        : JSON-serializable analysis data
            store_embedding: Whether to generate vector embedding

        Returns:
            str: UUID of the stored memory record

        Raises:
            DatabaseError: If storage operation fails
            ValueError: If memory_type is invalid
        """
        self._validate_memory_type(memory_type)

        # Check for existing record (upsert)
        existing = self._find_existing(candidate_id, memory_type)

        if existing:
            self._logger.info(
                "Updating existing memory | candidate=%s | type=%s",
                candidate_id, memory_type
            )
            return self.update_memory(
                memory_id=existing.id,
                content=content,
                store_embedding=store_embedding,
            )

        # Generate embedding if enabled
        embedding_id: Optional[str] = None
        if store_embedding and self._embeddings_enabled:
            embedding_id = self._store_embedding(content)

        # Create new record
        memory_id = str(uuid.uuid4())
        record = MemoryModel(
            id=memory_id,
            candidate_id=candidate_id,
            memory_type=memory_type,
            content=content,
            embedding_id=embedding_id,
        )

        with db_manager.get_session() as session:
            session.add(record)

        self._logger.info(
            "Memory stored | id=%s | candidate=%s | type=%s",
            memory_id, candidate_id, memory_type
        )
        return memory_id

    def get_memory(
        self,
        candidate_id: str,
        memory_type: str,
    ) -> Dict[str, Any]:
        """
        Retrieves a specific memory by candidate and type.

        Args:
            candidate_id: UUID of the candidate
            memory_type : Type of analysis result

        Returns:
            dict: Memory record with id, content, and metadata

        Raises:
            RecordNotFoundError: If memory not found
            ValueError: If memory_type is invalid
        """
        self._validate_memory_type(memory_type)

        with db_manager.get_session() as session:
            record = (
                session.query(MemoryModel)
                .filter(
                    MemoryModel.candidate_id == candidate_id,
                    MemoryModel.memory_type == memory_type,
                )
                .first()
            )

        if record is None:
            raise RecordNotFoundError(
                model="MemoryModel",
                identifier=f"{candidate_id}/{memory_type}",
            )

        return self._record_to_dict(record)

    def get_all_memories(
        self,
        candidate_id: str,
        *,
        memory_type: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Retrieves all memories for a candidate.

        Args:
            candidate_id: UUID of the candidate
            memory_type : Optional filter by type

        Returns:
            list[dict]: List of memory records
        """
        if memory_type:
            self._validate_memory_type(memory_type)

        with db_manager.get_session() as session:
            query = session.query(MemoryModel).filter(
                MemoryModel.candidate_id == candidate_id
            )

            if memory_type:
                query = query.filter(
                    MemoryModel.memory_type == memory_type
                )

            records = query.order_by(
                MemoryModel.created_at.desc()
            ).all()

        return [self._record_to_dict(r) for r in records]

    def update_memory(
        self,
        memory_id: str,
        content: Dict[str, Any],
        *,
        store_embedding: bool = True,
    ) -> str:
        """
        Updates an existing memory record.

        Args:
            memory_id      : UUID of the memory to update
            content        : New content data
            store_embedding: Whether to regenerate embedding

        Returns:
            str: UUID of the updated memory record

        Raises:
            RecordNotFoundError: If memory not found
            DatabaseError: If update operation fails
        """
        with db_manager.get_session() as session:
            record = session.query(MemoryModel).filter(
                MemoryModel.id == memory_id
            ).first()

            if record is None:
                raise RecordNotFoundError(
                    model="MemoryModel",
                    identifier=memory_id,
                )

            record.content = content

            # Update embedding if enabled
            if store_embedding and self._embeddings_enabled:
                embedding_id = self._store_embedding(content)
                record.embedding_id = embedding_id

        self._logger.info(
            "Memory updated | id=%s", memory_id
        )
        return memory_id

    def delete_memory(
        self,
        memory_id: str,
    ) -> bool:
        """
        Deletes a memory record by ID.

        Args:
            memory_id: UUID of the memory to delete

        Returns:
            bool: True if deleted successfully

        Raises:
            RecordNotFoundError: If memory not found
        """
        with db_manager.get_session() as session:
            record = session.query(MemoryModel).filter(
                MemoryModel.id == memory_id
            ).first()

            if record is None:
                raise RecordNotFoundError(
                    model="MemoryModel",
                    identifier=memory_id,
                )

            session.delete(record)

        self._logger.info("Memory deleted | id=%s", memory_id)
        return True

    def delete_candidate_memories(
        self,
        candidate_id: str,
    ) -> int:
        """
        Deletes all memories for a candidate.

        Args:
            candidate_id: UUID of the candidate

        Returns:
            int: Number of records deleted
        """
        with db_manager.get_session() as session:
            count = (
                session.query(MemoryModel)
                .filter(MemoryModel.candidate_id == candidate_id)
                .delete(synchronize_session="fetch")
            )

        self._logger.info(
            "Candidate memories deleted | candidate=%s | count=%d",
            candidate_id, count
        )
        return count

    # ── Vector Search ────────────────────────────────────────

    def search_similar(
        self,
        query_text: str,
        *,
        candidate_id: Optional[str] = None,
        top_k: int = 5,
    ) -> List[Dict[str, Any]]:
        """
        Searches for semantically similar memories using FAISS.

        Args:
            query_text  : Text to find similar memories for
            candidate_id: Optional filter to specific candidate
            top_k       : Number of results to return

        Returns:
            list[dict]: Ranked list of similar memory records
                        with similarity scores. Empty list if
                        embeddings are unavailable.
        """
        if not self._embeddings_enabled:
            self._logger.warning(
                "Vector search unavailable - embeddings disabled"
            )
            return []

        try:
            query_embedding = self._generate_embedding(query_text)
            if query_embedding is None:
                return []

            return self._faiss_search(
                query_embedding,
                candidate_id=candidate_id,
                top_k=top_k,
            )
        except Exception as exc:
            self._logger.error(
                "Vector search failed | error=%s", exc
            )
            return []

    # ── Private Helpers ──────────────────────────────────────

    def _validate_memory_type(self, memory_type: str) -> None:
        """
        Validates memory_type against allowed values.

        Raises:
            ValueError: If memory_type is not valid
        """
        if memory_type not in VALID_MEMORY_TYPES:
            raise ValueError(
                f"Invalid memory_type '{memory_type}'. "
                f"Must be one of: {sorted(VALID_MEMORY_TYPES)}"
            )

    def _find_existing(
        self,
        candidate_id: str,
        memory_type: str,
    ) -> Optional[MemoryModel]:
        """Finds existing memory record for candidate + type."""
        with db_manager.get_session() as session:
            return (
                session.query(MemoryModel)
                .filter(
                    MemoryModel.candidate_id == candidate_id,
                    MemoryModel.memory_type == memory_type,
                )
                .first()
            )

    def _record_to_dict(self, record: MemoryModel) -> Dict[str, Any]:
        """Converts a MemoryModel instance to a dictionary."""
        return {
            "id": record.id,
            "candidate_id": record.candidate_id,
            "memory_type": record.memory_type,
            "content": record.content,
            "embedding_id": record.embedding_id,
            "created_at": (
                record.created_at.isoformat()
                if record.created_at else None
            ),
        }

    # ── Embedding & FAISS ────────────────────────────────────

    def _init_vector_store(self) -> bool:
        """
        Initializes FAISS index for vector search.

        Returns:
            bool: True if vector store initialized successfully
        """
        try:
            import faiss

            index_path = self._vector_dir / "memory.index"
            map_path = self._vector_dir / "memory_map.json"

            self._vector_dir.mkdir(parents=True, exist_ok=True)

            if index_path.exists():
                self._faiss_index = faiss.read_index(
                    str(index_path)
                )
                if map_path.exists():
                    self._embedding_map = json.loads(
                        map_path.read_text(encoding="utf-8")
                    )
                self._logger.info(
                    "FAISS index loaded | vectors=%d",
                    self._faiss_index.ntotal
                )
            else:
                # Create new index (768 dims for Google embeddings)
                self._faiss_index = faiss.IndexFlatIP(768)
                self._embedding_map = {}
                self._logger.info("New FAISS index created | dims=768")

            self._index_initialized = True
            return True

        except ImportError:
            self._logger.warning(
                "FAISS not available - vector search disabled"
            )
            return False
        except Exception as exc:
            self._logger.warning(
                "Failed to initialize vector store | error=%s", exc
            )
            return False

    def _generate_embedding(
        self,
        text: str,
    ) -> Optional[np.ndarray]:
        """
        Generates embedding vector using Google GenAI.

        Args:
            text: Text to embed

        Returns:
            numpy array of embedding, or None on failure
        """
        try:
            from google import genai

            client = genai.Client(api_key=cfg.GOOGLE_API_KEY)

            # Truncate to avoid token limits
            truncated = text[:8000] if len(text) > 8000 else text

            result = client.models.embed_content(
                model="models/text-embedding-004",
                contents=truncated,
            )

            embedding = np.array(
                result.embeddings[0].values, dtype=np.float32
            )

            # Normalize for cosine similarity with IndexFlatIP
            norm = np.linalg.norm(embedding)
            if norm > 0:
                embedding = embedding / norm

            return embedding

        except Exception as exc:
            self._logger.warning(
                "Embedding generation failed | error=%s", exc
            )
            return None

    def _store_embedding(
        self,
        content: Dict[str, Any],
    ) -> Optional[str]:
        """
        Generates and stores embedding for content.

        Args:
            content: Memory content to embed

        Returns:
            str: Embedding ID, or None if embedding failed
        """
        if not self._index_initialized or self._faiss_index is None:
            return None

        # Convert content to text representation
        text = self._content_to_text(content)
        embedding = self._generate_embedding(text)

        if embedding is None:
            return None

        try:
            embedding_id = str(uuid.uuid4())
            index_position = self._faiss_index.ntotal

            # Add to FAISS index
            self._faiss_index.add(
                embedding.reshape(1, -1)
            )

            # Map embedding_id to index position
            self._embedding_map[embedding_id] = index_position

            # Persist index and mapping
            self._save_index()

            self._logger.debug(
                "Embedding stored | id=%s | position=%d",
                embedding_id, index_position
            )
            return embedding_id

        except Exception as exc:
            self._logger.warning(
                "Failed to store embedding | error=%s", exc
            )
            return None

    def _faiss_search(
        self,
        query_embedding: np.ndarray,
        *,
        candidate_id: Optional[str] = None,
        top_k: int = 5,
    ) -> List[Dict[str, Any]]:
        """
        Performs FAISS similarity search and returns matching memories.

        Args:
            query_embedding: Query vector
            candidate_id   : Optional candidate filter
            top_k          : Number of results

        Returns:
            list[dict]: Matching memories with similarity scores
        """
        if self._faiss_index is None or self._faiss_index.ntotal == 0:
            return []

        # Search more than top_k to account for filtering
        search_k = min(top_k * 3, self._faiss_index.ntotal)

        scores, indices = self._faiss_index.search(
            query_embedding.reshape(1, -1),
            search_k,
        )

        # Reverse map: position -> embedding_id
        position_to_id = {
            v: k for k, v in self._embedding_map.items()
        }

        results: List[Dict[str, Any]] = []

        with db_manager.get_session() as session:
            for score, idx in zip(scores[0], indices[0]):
                if idx == -1:
                    continue

                embedding_id = position_to_id.get(int(idx))
                if embedding_id is None:
                    continue

                query = session.query(MemoryModel).filter(
                    MemoryModel.embedding_id == embedding_id
                )

                if candidate_id:
                    query = query.filter(
                        MemoryModel.candidate_id == candidate_id
                    )

                record = query.first()
                if record is None:
                    continue

                result = self._record_to_dict(record)
                result["similarity_score"] = float(score)
                results.append(result)

                if len(results) >= top_k:
                    break

        return results

    def _save_index(self) -> None:
        """Persists FAISS index and embedding map to disk."""
        try:
            import faiss

            index_path = self._vector_dir / "memory.index"
            map_path = self._vector_dir / "memory_map.json"

            faiss.write_index(self._faiss_index, str(index_path))
            map_path.write_text(
                json.dumps(self._embedding_map),
                encoding="utf-8",
            )
        except Exception as exc:
            self._logger.warning(
                "Failed to save FAISS index | error=%s", exc
            )

    @staticmethod
    def _content_to_text(content: Dict[str, Any]) -> str:
        """
        Converts content dictionary to a text representation
        suitable for embedding generation.

        Args:
            content: Dictionary to convert

        Returns:
            str: Flattened text representation
        """
        parts: List[str] = []

        for key, value in content.items():
            if isinstance(value, str):
                parts.append(f"{key}: {value}")
            elif isinstance(value, (list, dict)):
                parts.append(f"{key}: {json.dumps(value)}")
            elif value is not None:
                parts.append(f"{key}: {value}")

        return " | ".join(parts)
