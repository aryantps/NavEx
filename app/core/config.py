from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost/postgres"
    USE_UVICORN_LOGGER: bool = False
    LOG_LEVEL: str = "INFO"

    # class Config:
    #     env_file = ".env"



settings = Settings()