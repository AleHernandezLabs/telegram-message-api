from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database configuration
    database_url: str

    # Security and authentication
    api_key: str

    # Author information (to be used in the API responses)
    author: str = "Alejandro Exequiel Hernández Lara"
    website: str = "www.alehernandezlabs.com"
    email: str = "alehernandezlabs@gmail.com"

    # Application metadata
    app_name: str = "Telegram Message API"
    app_version: str = "1.0.0"

    # Logging configuration
    log_level: str = "INFO"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
