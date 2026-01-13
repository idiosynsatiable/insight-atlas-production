from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyHttpUrl
from typing import List

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # Database
    DATABASE_URL: str = "sqlite:///./data/atlas.db"
    
    # Security
    JWT_SECRET: str = "change_me"
    
    # Mode
    DEMO_MODE: bool = True
    
    # CORS
    CORS_ORIGINS: str = "http://localhost:3000"
    
    # App
    APP_BASE_URL: str = "http://localhost:3000"
    
    # Stripe
    STRIPE_SECRET_KEY: str | None = None
    STRIPE_WEBHOOK_SECRET: str | None = None
    STRIPE_PRICE_PRO_MONTHLY: str | None = None
    STRIPE_PRICE_YEARLY: str | None = None

    # OpenAI
    OPENAI_API_KEY: str | None = None
    OPENAI_MODEL: str = "gpt-4.1-mini"
    OPENAI_POLISH_ENABLED: bool = False

    # Rate limiting
    RATE_LIMIT_RPM: int = 60
    
    # Observability
    SENTRY_DSN: str | None = None
    LOG_LEVEL: str = "INFO"

settings = Settings()
