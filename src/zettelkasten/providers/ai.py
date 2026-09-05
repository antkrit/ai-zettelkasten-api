from typing import Protocol, runtime_checkable

from zettelkasten.models.ai import GeneratedNote, NoteGenerationRequest


@runtime_checkable
class AIProvider(Protocol):
    """Abstract AI backend for summarizing source material into notes."""

    async def generate_note(self, request: NoteGenerationRequest) -> GeneratedNote:
        """Summarize content and propose tags for implicit linking."""
        ...


class MockAIProvider:
    """Deterministic stand-in: short summary-style body and simple tag extraction."""

    async def generate_note(self, request: NoteGenerationRequest) -> GeneratedNote:
        source = request.content.strip()
        title = self._derive_title(source)
        tags = self._derive_tags(source)
        content = self._summarize(source)

        return GeneratedNote(title=title, content=content, tags=tags)

    def _derive_title(self, content: str) -> str:
        first_line = content.splitlines()[0] if content else "Untitled note"
        title = first_line.lstrip("# ").strip()
        if len(title) > 80:
            title = f"{title[:77].rstrip()}…"
        return title or "Untitled note"

    def _derive_tags(self, content: str) -> list[str]:
        words = {
            word.strip("#.,!?;:()[]{}\"'").lower()
            for word in content.split()
            if len(word.strip("#.,!?;:()[]{}\"'")) > 4
        }
        return sorted(words)[:5]

    def _summarize(self, content: str) -> str:
        if not content:
            return ""
        # Stand-in for a real model summary: keep the opening passage.
        max_len = 280
        if len(content) <= max_len:
            return content
        return f"{content[:max_len].rstrip()}…"
