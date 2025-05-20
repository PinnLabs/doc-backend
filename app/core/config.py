from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXP_SECONDS: int = 3600
    STRIPE_SECRET_KEY: str
    STRIPE_PRICE_ID_STARTER: str
    STRIPE_PRICE_ID_PRO: str
    STRIPE_PRICE_ID_UNLIMITED: str
    FRONTEND_URL: str
    SUPABASE_URL: str
    SUPABASE_KEY: str
    FIREBASE_CREDENTIALS: str = (
        "app/doccrafter-544cf-firebase-adminsdk-fbsvc-368172c6d5.json"
    )
    DEBUG: bool = False
    ENV: str = "production"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


@lru_cache()
def get_settings():
    return Settings()
