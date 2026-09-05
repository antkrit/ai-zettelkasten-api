from pydantic import BaseModel, Field


class Note(BaseModel):
    """Atomic Zettelkasten note. Related notes are found via shared tags in Notion."""

    title: str
    content: str
    tags: list[str] = Field(default_factory=list)
    # Notion page id after persistence; Notion remains the source of truth.
    external_id: str | None = None
