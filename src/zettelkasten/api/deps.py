from collections.abc import Callable

from zettelkasten.providers import AIProvider, MockAIProvider

# Swap this callable to inject a real provider later
_ai_provider_factory: Callable[[], AIProvider] = MockAIProvider


def get_ai_provider() -> AIProvider:
    return _ai_provider_factory()


def set_ai_provider_factory(factory: Callable[[], AIProvider]) -> None:
    global _ai_provider_factory
    _ai_provider_factory = factory
