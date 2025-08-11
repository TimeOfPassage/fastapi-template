import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "fastapi_project"
    DATABASE_URL: str = "sqlite:///./test.db"
    LOG_LEVEL: str = "DEBUG"
    if not os.path.exists("logs"):
        os.makedirs("logs")
    LOG_FILE: str = "logs/app.log"

    class Config:
        env_file = ".env"


settings = Settings()
# print(settings.PROJECT_NAME)  # 输出: My FastAPI Project
# print(settings.DATABASE_URL)  # 输出: postgresql://user:password@localhost:5432/mydb

__all__ = ["settings"]
