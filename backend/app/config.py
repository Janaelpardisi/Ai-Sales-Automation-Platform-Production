"""
Application Configuration
"""

from functools import lru_cache
from pathlib import Path
from typing import Optional
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings"""
    
    # App
    APP_NAME: str = "AI Sales Agent"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    ENVIRONMENT: str = "development"
    
    # API
    API_V1_PREFIX: str = "/api/v1"
    SECRET_KEY: str = "change-this-secret-key-min-32-chars"
    
    # CORS
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:8000", "null", "*"]
    
    # Database - Default path on D: drive
    DATABASE_URL: str = "sqlite+aiosqlite:///D:/Ai_Sales_Agent/data/sales_agent.db"
    DB_ECHO: bool = False
    
    # Gemini API
    GEMINI_API_KEY: str = Field(default="", description="Google Gemini API key")
    GEMINI_MODEL: str = "gemini-pro"
    GEMINI_TEMPERATURE: float = 0.7
    GEMINI_MAX_TOKENS: int = 2048
    
    # Email
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM_EMAIL: str = ""
    SMTP_FROM_NAME: str = "AI Sales Agent"
    
    # Scraping
    PLAYWRIGHT_HEADLESS: bool = True
    SCRAPING_DELAY: float = 1.0
    MAX_CONCURRENT_SCRAPES: int = 5
    USER_AGENT: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    
    # Agent Settings
    MAX_RESEARCH_RESULTS: int = 50
    QUALIFICATION_THRESHOLD: float = 0.7
    MAX_FOLLOW_UPS: int = 3
    FOLLOW_UP_DELAYS: list[int] = [3, 7, 14]
    
    # Paths - Default on D: drive
    DATA_DIR: str = "D:/Ai_Sales_Agent/data"
    LOGS_DIR: str = "D:/Ai_Sales_Agent/logs"
    CHROMA_PERSIST_DIRECTORY: str = "D:/Ai_Sales_Agent/data/chroma"
    
    # SerpAPI (Real Company Search)
    SERPAPI_KEY: str = ""
    USE_REAL_SEARCH: bool = False
    
    # Email Finding APIs
    HUNTER_API_KEY: str = ""
    SNOV_API_KEY: str = ""  # Snov.io API key
    APOLLO_API_KEY: str = ""  # Apollo.io API key
    USE_REAL_EMAILS: bool = False
    
    # Monitoring
    LOG_LEVEL: str = "INFO"
    
    model_config = SettingsConfigDict(
        env_file=str(Path(__file__).parent.parent / ".env"),
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )
    
    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v):
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        return v


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()