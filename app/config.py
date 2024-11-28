from pydantic_settings import BaseSettings
from typing import List
import os
from dotenv import load_dotenv
from functools import lru_cache

# Load environment variables
load_dotenv()

class Settings(BaseSettings):
    # API Settings
    api_version: str = os.getenv("API_VERSION", "v1")
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"
    secret_key: str = os.getenv("SECRET_KEY", "your-secret-key-change-this-in-production")
    
    # Server Settings
    host: str = os.getenv("HOST", "0.0.0.0")
    port: int = int(os.getenv("PORT", "8000"))
    workers: int = int(os.getenv("WORKERS", "4"))
    
    # Rate Limiting
    rate_limit_per_minute: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", "100"))
    
    # Model Settings
    batch_size: int = int(os.getenv("BATCH_SIZE", "32"))
    max_workers: int = int(os.getenv("MAX_WORKERS", "8"))
    
    # Logging
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Security
    allow_origins: List[str] = os.getenv("ALLOW_ORIGINS", '["*"]').strip('[]').replace('"', '').split(',')
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @property
    def cors_origins(self) -> List[str]:
        return [origin.strip() for origin in self.allow_origins]

@lru_cache()
def get_settings() -> Settings:
    return Settings()