import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    PORT: int = int(os.getenv("PORT", "3001"))
    ENV: str = os.getenv("ENV", "development")
    API_VERSION: str = os.getenv("API_VERSION", "v1")
    CORS_ORIGINS: str = os.getenv("CORS_ORIGINS", "*")
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "Multi-Agent Decision Engine")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://tamildev:123_TamiL_321@localhost:5422/multi_agent")

    class Config:
        case_sensitive = True

settings = Settings()