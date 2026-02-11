"""
Logging Configuration
"""

import logging
import sys
from pathlib import Path
from app.config import settings


def setup_logging():
    """Setup application logging"""
    
    # Create logs directory if it doesn't exist
    log_dir = Path(settings.LOGS_DIR)
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Configure root logger
    logging.basicConfig(
        level=getattr(logging, settings.LOG_LEVEL),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            # Console handler
            logging.StreamHandler(sys.stdout),
            # File handler
            logging.FileHandler(log_dir / "app.log")
        ]
    )
    
    # Set specific loggers
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    
    return logging.getLogger(__name__)


logger = setup_logging()