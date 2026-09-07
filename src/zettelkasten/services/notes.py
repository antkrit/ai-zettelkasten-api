import json
from typing import Any

from zettelkasten.clients.base import KnowledgeBaseClient
from zettelkasten.models.ai import NoteGenerationRequest
from zettelkasten.models.job import NoteJob
from zettelkasten.models.note import Note
from zettelkasten.providers.ai import AIProvider


async def process_note_job(
    job: NoteJob,
    *,
    ai: AIProvider,
    knowledge_base: KnowledgeBaseClient,
) -> Note:
    """Generate a note and store it in the knowledge base."""
    draft = await ai.generate_note(NoteGenerationRequest(content=job.content))
    return await knowledge_base.create_note(draft)


def parse_note_job(body: str | dict[str, Any]) -> NoteJob:
    if isinstance(body, str):
        return NoteJob.model_validate(json.loads(body))
    return NoteJob.model_validate(body)
