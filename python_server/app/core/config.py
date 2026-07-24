import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    PORT: int = int(os.getenv("PORT", "3001"))
    ENV: str = os.getenv("ENV", "development")
    API_VERSION: str = os.getenv("API_VERSION", "v1")
    CORS_ORIGINS: str = os.getenv("CORS_ORIGINS", "*")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/multi_agent_db")
    PROJECT_NAME: str = "Multiagent"
    class Config:
        case_sensitive = True

settings = Settings()