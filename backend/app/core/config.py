from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    mongodb_url: str = "mongodb://localhost:27017"
    database_name: str = "storyteller"

    class Config:
        env_file = ".env"


settings = Settings()
