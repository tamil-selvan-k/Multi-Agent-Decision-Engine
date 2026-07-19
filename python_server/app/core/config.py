import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    PORT: int = int(os.getenv("PORT"))
    ENV: str = os.getenv("ENV")
    API_VERSION: str = os.getenv("API_VERSION")
    CORS_ORIGINS: str = os.getenv("CORS_ORIGINS")
    PROJECT_NAME: str = "Multi-Agent Decision Engine"
    DATABASE_URL: str = os.getenv("DATABASE_URL")

settings = Settings()
