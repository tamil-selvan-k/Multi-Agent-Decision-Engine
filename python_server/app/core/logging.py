import logging
import sys
import os
from logging.handlers import RotatingFileHandler
from core.config import settings

# Create logs directory if it doesn't exist
os.makedirs("logs", exist_ok=True)

class CustomFormatter(logging.Formatter):
    """Custom formatting for the AI Microservice logging."""
    def format(self, record):
        return super().format(record)

def setup_logging():
    logger = logging.getLogger("multi_agent")
    
    # Set base level
    level = logging.DEBUG if settings.ENV == "development" else logging.INFO
    logger.setLevel(level)

    # Prevent duplicate logs if already configured
    if not logger.handlers:
        # Console Formatter
        console_formatter = logging.Formatter(
            '%(asctime)s [%(levelname)s]: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # File Formatter (JSON-like or detailed)
        file_formatter = logging.Formatter(
            '{"time": "%(asctime)s", "level": "%(levelname)s", "module": "%(name)s", "message": "%(message)s"}'
        )

        # Console Handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

        # Combined File Handler
        combined_file_handler = RotatingFileHandler(
            "logs/combined.log", maxBytes=5*1024*1024, backupCount=2
        )
        combined_file_handler.setFormatter(file_formatter)
        logger.addHandler(combined_file_handler)

        # Error File Handler
        error_file_handler = RotatingFileHandler(
            "logs/error.log", maxBytes=5*1024*1024, backupCount=2
        )
        error_file_handler.setLevel(logging.ERROR)
        error_file_handler.setFormatter(file_formatter)
        logger.addHandler(error_file_handler)

    return logger

logger = setup_logging()
