from enum import StrEnum

from pydantic import BaseModel, Field


class AIProviderName(StrEnum):
    DEEPSEEK = "deepseek"
    MOCK = "mock"


class KnowledgeBaseClientName(StrEnum):
    NOTION = "notion"
    MOCK = "mock"


class NoteJob(BaseModel):
    """SQS payload: source material and backend selectors.

    Selectors name which implementation to use; secrets stay in worker env/settings.
    """

    content: str = Field(min_length=1)
    ai_provider: AIProviderName = AIProviderName.DEEPSEEK
    knowledge_base: KnowledgeBaseClientName = KnowledgeBaseClientName.NOTION
