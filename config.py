import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
env_path = BASE_DIR / ".env"

if env_path.exists():
    load_dotenv(env_path)


class BaseConfig:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-change-this-key")

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "SQLALCHEMY_DATABASE_URI",
        f"sqlite:///{BASE_DIR / 'hospital_management.sqlite3'}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "hospital_management_db")

    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = False

    STROKE_DATA_PATH = os.getenv(
        "STROKE_DATA_PATH",
        str(BASE_DIR / "dataset" / "stroke_data.csv")
    )


class DevelopmentConfig(BaseConfig):
    DEBUG = True


config_map = {
    "development": DevelopmentConfig,
    "default": DevelopmentConfig,
}
