from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):

    # -----------------------------
    # APPLICATION
    # -----------------------------
    APP_NAME: str = "DineVibe Backend"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # -----------------------------
    # DATABASE
    # -----------------------------
    DATABASE_URL: str

    # -----------------------------
    # SECURITY
    # -----------------------------
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # -----------------------------
    # OTP
    # -----------------------------
    OTP_EXPIRY_SECONDS: int = 300
    # -----------------------------
    # SMS (TWILIO)
    # -----------------------------
    TWILIO_ACCOUNT_SID: str
    TWILIO_AUTH_TOKEN: str
    TWILIO_PHONE_NUMBER: str

    # -----------------------------
    # -----------------------------
    # EMAIL (BREVO)
    # -----------------------------
    BREVO_API_KEY: str
    SENDER_EMAIL: str

    # -----------------------------
    # CORS
    # -----------------------------
    ALLOWED_ORIGINS: List[str] = ["*"]

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
