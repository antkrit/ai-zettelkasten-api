import asyncio
import json

from deepseek import DeepSeekAPI

from zettelkasten.models.ai import GeneratedNote, NoteGenerationRequest
from zettelkasten.providers.ai import AIProvider

_SYSTEM_PROMPT = """\
You are an assistant that converts study material into a single atomic Zettelkasten note.

Return a JSON object only. Do not use markdown fences or any text outside the JSON object.

Schema:
{
  "title": "concise title expressing the main idea",
  "content": "self-contained explanation of the idea",
  "tags": ["lowercase", "concise", "topic", "tags"]
}

Rules:
- Extract one atomic idea from the source.
- Focus on the most useful and reusable idea, not a general summary of the entire source.
- The note must be understandable on its own without requiring the reader to see the original source.
- Preserve important nuance and qualifications from the source.
- Do not invent facts, examples, interpretations, or conclusions that are not supported by the source.
- Prefer precise language over vague generalizations.
- Use markdown only inside the "content" field when useful.
- Use 3–8 concise, lowercase tags that describe the concepts discussed in the note.
- Do not include generic tags such as "note", "study", or "information".
"""


class DeepSeekProvider(AIProvider):
    """AIProvider backed by the DeepSeek chat completions API."""

    def __init__(self, api_key: str, *, model: str = "deepseek-chat") -> None:
        if not api_key:
            raise ValueError("DeepSeek api_key is required")
        self._client = DeepSeekAPI(api_key)
        self._model = model

    async def generate_note(self, request: NoteGenerationRequest) -> GeneratedNote:
        raw = await asyncio.to_thread(self._complete, request.content)
        return self._parse(raw)

    def _complete(self, content: str) -> str:
        result = self._client.chat_completion(
            prompt=content,
            prompt_sys=_SYSTEM_PROMPT,
            model=self._model,
            stream=False,
            temperature=0.3,
            response_format={"type": "json_object"},
        )
        if not isinstance(result, str):
            raise TypeError(
                f"Expected str from DeepSeek chat_completion, got {type(result)!r}"
            )
        return result

    def _parse(self, raw: str) -> GeneratedNote:
        try:
            data = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise ValueError(f"DeepSeek returned invalid JSON: {raw[:500]!r}") from exc

        return GeneratedNote.model_validate(data)
