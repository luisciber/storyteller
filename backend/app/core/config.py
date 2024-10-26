from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    project_name: str = "Storyteller API"
    mongodb_url: str = ""
    database_name: str = "storyteller"
    openai_api_key: str = ""
    anthropic_api_key: str = ""
    gcp_project_id: str = ""
    bucket_url: str = ""
    bucket_name: str = ""
    replicate_api_token: str = ""

    class Config:
        env_file = ".env"


settings = Settings()
