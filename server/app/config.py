import os
from typing import Optional

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    BASE_URI: Optional[str] = os.environ.get("BASE_URI")
    HOST: Optional[str] = os.environ.get("HOST")
    PORT: Optional[str] = os.environ.get("PORT")

    DB_HOST: Optional[str] = os.environ.get("BASE_URI")
    DB_PORT: Optional[str] = os.environ.get("DB_PORT")
    DB_USER: Optional[str] = os.environ.get("DB_USER")
    DB_PASS: Optional[str] = os.environ.get("DB_PASS")
    DB_NAME: Optional[str] = os.environ.get("DB_NAME")

    DB_HOST_TEST: Optional[str] = os.environ.get("DB_HOST_TEST")
    DB_PORT_TEST: Optional[str] = os.environ.get("DB_PORT_TEST")
    DB_USER_TEST: Optional[str] = os.environ.get("DB_USER_TEST")
    DB_PASS_TEST: Optional[str] = os.environ.get("DB_PASS_TEST")
    DB_NAME_TEST: Optional[str] = os.environ.get("DB_NAME_TEST")

    @property
    def database_url_asyncpg(self):
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    @property
    def database_test_url_asyncpg(self):
        return (
            f"postgresql+asyncpg://{self.DB_USER_TEST}:{self.DB_PASS_TEST}"
            f"@{self.DB_HOST_TEST}:{self.DB_PORT_TEST}/{self.DB_NAME_TEST}"
        )


setting = Settings()
