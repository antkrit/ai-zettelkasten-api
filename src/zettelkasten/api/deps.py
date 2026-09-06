from enum import StrEnum

from zettelkasten.api.config import settings
from zettelkasten.providers import AIProvider, DeepSeekProvider, MockAIProvider


class AIProviderName(StrEnum):
    DEEPSEEK = "deepseek"
    MOCK = "mock"


class AIProviderFactory:
    """Build concrete AIProvider instances from an allowlisted name."""

    def __init__(self, model: AIProviderName =AIProviderName.DEEPSEEK) -> None:
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
