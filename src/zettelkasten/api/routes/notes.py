from typing import Annotated

from fastapi import APIRouter, Depends

from zettelkasten.api.deps import AIProviderFactory, AIProviderName
from zettelkasten.models import GeneratedNote, NoteGenerationRequest
from zettelkasten.providers import AIProvider

router = APIRouter(prefix="/notes", tags=["notes"])


@router.post("/generate", response_model=GeneratedNote)
async def generate_note(
    request: NoteGenerationRequest,
    provider: Annotated[AIProvider, Depends(AIProviderFactory(AIProviderName.DEEPSEEK))],
) -> GeneratedNote:
    """Summarize source material into a note draft with tags."""
    return await provider.generate_note(request)
