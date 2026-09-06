from typing import Self

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class DeepSeekSettings(BaseSettings):
    """DeepSeek API credentials and model selection (`DEEPSEEK_*` env vars)."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="DEEPSEEK_",
        extra="ignore",
    )

    api_key: str = ""
    api_url: str = "https://api.deepseek.com"
    api_model: str = "deepseek-v4-pro"

    @model_validator(mode="after")
    def _require_api_key(self) -> Self:
        if not self.api_key:
            raise ValueError("DEEPSEEK_API_KEY is required")
        return self


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    allowed_origins: list[str] = ["http://localhost"]
    deepseek: DeepSeekSettings = Field(default_factory=DeepSeekSettings)


settings = Settings()
