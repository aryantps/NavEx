from pathlib import Path
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost/postgres"
    USE_UVICORN_LOGGER: bool = False
    LOG_LEVEL: str = "INFO"


    AUTH_ALGORITHM: str = "RS256"
    AUTH_PUBLIC_KEY_FILE_PATH: str
    AUTH_PUBLIC_KEY: str = ""
    AUTH_AUDIENCE: str
    AUTH_ISSUER: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.AUTH_PUBLIC_KEY = self._load_public_key(self.AUTH_PUBLIC_KEY_FILE_PATH)

    def _load_public_key(self, path: str) -> str:
        try:
            return Path(path).read_text().strip()
        except Exception as e:
            raise ValueError(f"Failed to read JWT secret key from file '{path}': {e}") from e




settings = Settings()