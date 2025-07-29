"""Configuration module for Vibe Math API"""

import os
from typing import Optional
from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    """Application settings with validation"""
    
    # API Configuration
    gemini_api_key: str = Field(..., env="GEMINI_API_KEY")
    model_name: str = Field(default="gemini-1.5-flash", env="MODEL_NAME")
    max_tokens: int = Field(default=500, env="MAX_TOKENS")
    temperature: float = Field(default=0.2, env="TEMPERATURE")
    
    # Server Configuration
    host: str = Field(default="0.0.0.0", env="HOST")
    port: int = Field(default=8000, env="PORT")
    
    # Logging Configuration
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    
    # Security
    cors_origins: list = Field(default=["*"], env="CORS_ORIGINS")
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Create settings instance
settings = Settings()

# Validate critical settings
if not settings.gemini_api_key:
    raise ValueError("GEMINI_API_KEY is required")

# Export commonly used settings
GEMINI_API_KEY = settings.gemini_api_key
MODEL_NAME = settings.model_name
MAX_TOKENS = settings.max_tokens
TEMPERATURE = settings.temperature
HOST = settings.host
PORT = settings.port
LOG_LEVEL = settings.log_level