from typing import Annotated

from fastapi import APIRouter, Depends

from zettelkasten.api.deps import (
    AIProviderFactory,
    AIProviderName,
    KnowledgeBaseClientFactory,
    KnowledgeBaseClientName,
)
from zettelkasten.clients import KnowledgeBaseClient
from zettelkasten.models import Note, NoteGenerationRequest
from zettelkasten.providers import AIProvider

router = APIRouter(prefix="/notes", tags=["notes"])


@router.post("/generate", response_model=Note)
async def generate_note(
    request: NoteGenerationRequest,
    ai: Annotated[AIProvider, Depends(AIProviderFactory(AIProviderName.DEEPSEEK))],
    knowledge_base: Annotated[
        KnowledgeBaseClient,
        Depends(KnowledgeBaseClientFactory(KnowledgeBaseClientName.NOTION)),
    ],
) -> Note:
    """Summarize source material and store the note in the knowledge base."""
    draft = await ai.generate_note(request)
    return await knowledge_base.create_note(draft)
