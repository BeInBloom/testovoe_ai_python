from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppConfig(BaseSettings):
    openrouter_api_key: str = ""
    openrouter_model: str = "google/gemini-2.0-flash-exp:free"
    max_file_size_mb: int = 10
    skills_path: str = "src/skills/.config/happy_smile"
    prompts_path: str = "base_prompts"
    recursive_scan: bool = True
    request_timeout: int = 60
    max_retries: int = 3

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8", 
        extra="ignore"
    )
