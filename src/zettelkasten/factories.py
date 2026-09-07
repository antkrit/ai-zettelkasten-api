from zettelkasten.clients import (
    KnowledgeBaseClient,
    MockKnowledgeBaseClient,
    NotionClient,
)
from zettelkasten.config import settings
from zettelkasten.models.job import AIProviderName, KnowledgeBaseClientName
from zettelkasten.providers import AIProvider, DeepSeekProvider, MockAIProvider


class AIProviderFactory:
    """Build concrete AIProvider instances from an allowlisted name."""

    def __init__(self, model: AIProviderName = AIProviderName.DEEPSEEK) -> None:
        self.model = model

    def __call__(self) -> AIProvider:
        match self.model:
            case AIProviderName.DEEPSEEK:
                return DeepSeekProvider(
                    api_key=settings.deepseek.api_key,
                    model=settings.deepseek.api_model,
                )
            case AIProviderName.MOCK:
                return MockAIProvider()
            case _:
                raise ValueError(f"Unsupported AI provider: {self.model!r}")


class KnowledgeBaseClientFactory:
    """Build concrete KnowledgeBaseClient instances from an allowlisted name."""

    def __init__(
        self, backend: KnowledgeBaseClientName = KnowledgeBaseClientName.NOTION
    ) -> None:
        self.backend = backend

    def __call__(self) -> KnowledgeBaseClient:
        match self.backend:
            case KnowledgeBaseClientName.NOTION:
                return NotionClient(
                    api_key=settings.notion.api_key,
                    database_id=settings.notion.database_id,
                    title_property=settings.notion.title_property,
                    tags_property=settings.notion.tags_property,
                )
            case KnowledgeBaseClientName.MOCK:
                return MockKnowledgeBaseClient()
            case _:
                raise ValueError(f"Unsupported knowledge base client: {self.backend!r}")
