import os

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    project_name: str = "Storyteller API"
    mongodb_url: str = Field(default=os.getenv("MONGODB_URL"))
    database_name: str = Field(default=os.getenv("DATABASE_NAME"))
    openai_api_key: str = Field(default=os.getenv("OPENAI_API_KEY"))
    gcp_project_id: str = Field(default=os.getenv("GCP_PROJECT_ID"))
    bucket_url: str = Field(default=os.getenv("BUCKET_URL"))
    bucket_name: str = Field(default=os.getenv("BUCKET_NAME"))
    replicate_api_token: str = Field(default=os.getenv("REPLICATE_API_TOKEN"))
    development: bool = Field(default=os.getenv("DEVELOPMENT") == "true")

    model_config = SettingsConfigDict()


settings = Settings()
