from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    DEBUG: str
    SECRET_KEY: str

    class Config:
        # env_file = ".env"
        env_file = os.path.join(os.path.dirname(__file__), ".env")  # points to config/.env

settings = Settings()