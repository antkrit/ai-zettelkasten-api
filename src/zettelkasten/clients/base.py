from typing import Protocol, runtime_checkable
from uuid import uuid4

from zettelkasten.models.ai import GeneratedNote
from zettelkasten.models.note import Note


@runtime_checkable
class KnowledgeBaseClient(Protocol):
    """Abstract client for persisting Zettelkasten notes (e.g. Notion)."""

    async def create_note(self, note: GeneratedNote) -> Note:
        """Persist a generated note and return it with an external id."""
        ...


class MockKnowledgeBaseClient:
    """In-memory stand-in that assigns a fake external id."""

    async def create_note(self, note: GeneratedNote) -> Note:
        return Note(
            title=note.title,
            content=note.content,
            tags=list(note.tags),
            external_id=f"mock-{uuid4()}",
        )
