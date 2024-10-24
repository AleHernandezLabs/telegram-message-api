import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost/dbname')
    API_KEY: str = os.getenv('API_KEY', 'your_production_api_key')

    class Config:
        env_file = ".env"

settings = Settings()