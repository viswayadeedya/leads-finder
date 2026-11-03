from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    google_api_key: SecretStr
    groq_api_key: SecretStr
    llm_model: str
    llm_timeout_seconds: float = 30
    http_timeout_seconds: float = 10
    max_retries: int = 3
    max_tokens: int = 1000
    temperature: float = 0.2

settings = Settings() # type: ignore[call-arg]


