from urllib.parse import urlparse, parse_qs, urlunparse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

def clean_database_url(url: str) -> str:
    """Strips Prisma-specific query params (schema, connection_limit) that cause psycopg2 DSN errors."""
    if not url:
        return url
    parsed = urlparse(url)
    if not parsed.query:
        return url
    
    allowed_params = {'sslmode', 'target_session_attrs', 'application_name'}
    query_params = parse_qs(parsed.query)
    filtered = {k: v for k, v in query_params.items() if k.lower() in allowed_params}
    
    new_query = "&".join([f"{k}={v[0]}" for k, v in filtered.items()])
    return urlunparse(parsed._replace(query=new_query))

db_url = clean_database_url(settings.DATABASE_URL)

# Create SQLAlchemy engine
engine = create_engine(
    db_url,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20
)

# Session factory for DB transactions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declarative base class for models
Base = declarative_base()

def get_db():
    """
    FastAPI dependency that provides a transactional database session per request.
    Automatically closes session upon request completion.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
