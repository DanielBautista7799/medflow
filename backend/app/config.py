"""
MedFlow Command Center
Day 11 - centralized application settings.

Replaces the scattered os.environ.get() calls that were previously
inside database.py, security.py, and main.py.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = (
        "postgresql+asyncpg://danielbautista@127.0.0.1:5432/medflow_dev"
    )

    secret_key: str

    frontend_origin: str = "http://localhost:5173"

    # Read values from backend/.env and replace here
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()