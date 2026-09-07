from notion_client import AsyncClient

from zettelkasten.clients.base import KnowledgeBaseClient
from zettelkasten.models.ai import GeneratedNote
from zettelkasten.models.note import Note

# Notion rich_text content chunks are capped at 2000 characters.
_MAX_RICH_TEXT = 2000


class NotionClient(KnowledgeBaseClient):
    """Persist notes as rows in a Notion database."""

    def __init__(
        self,
        api_key: str,
        *,
        database_id: str,
        title_property: str = "Name",
        tags_property: str = "Tags",
    ) -> None:
        if not api_key:
            raise ValueError("Notion api_key is required")
        if not database_id:
            raise ValueError("Notion database_id is required")
        self._client = AsyncClient(auth=api_key)
        self.database_id = database_id
        self.title_property = title_property
        self.tags_property = tags_property

    async def create_note(self, note: GeneratedNote) -> Note:
        response = await self._client.pages.create(
            parent={"database_id": self.database_id},
            properties=self._properties(note),
        )
        page_id = response["id"]
        if not isinstance(page_id, str):
            raise TypeError(f"Unexpected Notion page id type: {type(page_id)!r}")

        blocks = self._content_blocks(note.content)
        if blocks:
            await self._client.blocks.children.append(page_id, children=blocks)

        return Note(
            title=note.title,
            content=note.content,
            tags=list(note.tags),
            external_id=page_id,
        )

    def _properties(self, note: GeneratedNote) -> dict:
        return {
            self.title_property: {
                "title": [{"type": "text", "text": {"content": note.title[:_MAX_RICH_TEXT]}}],
            },
            self.tags_property: {
                "multi_select": [{"name": tag} for tag in note.tags],
            },
        }

    def _content_blocks(self, content: str) -> list[dict]:
        blocks: list[dict] = []
        paragraphs = content.split("\n\n") if content.strip() else [""]
        for paragraph in paragraphs:
            text = paragraph.strip() or " "
            for start in range(0, len(text), _MAX_RICH_TEXT):
                chunk = text[start : start + _MAX_RICH_TEXT]
                blocks.append(
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [
                                {"type": "text", "text": {"content": chunk}},
                            ],
                        },
                    }
                )
        return blocks
