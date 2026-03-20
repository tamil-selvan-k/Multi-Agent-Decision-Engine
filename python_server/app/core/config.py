import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PORT: int = 3001
    ENV: str = "development"
    API_VERSION: str = "v1"
    CORS_ORIGINS: str = "*"
    PROJECT_NAME: str = "PS10 Multi-Agent Decision Engine"
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
