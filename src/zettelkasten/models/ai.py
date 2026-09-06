from pydantic import BaseModel, Field


class NoteGenerationRequest(BaseModel):
    """Raw source material to summarize into a Zettelkasten note.

    Today this is plain text; later it can be text extracted from a PDF or
    other study material before calling the AI provider.
    """

    content: str


class GeneratedNote(BaseModel):
    """AI-produced note draft: summary plus tags for implicit linking."""

    title: str = Field(min_length=1)
    content: str = Field(min_length=1)
    tags: list[str] = Field(default_factory=list, min_length=1, max_length=8)
