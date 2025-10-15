from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # App Setting
    APP_NAME: str = "Chat-Quest"
    DEBUG: bool = False

    # OpenAI Setting
    OPENAI_API_KEY: str = ''

    # DB Setting
    DB_USER: str = ''
    DB_PASSWORD: str = ''
    DB_HOST: str = ''
    DB_PORT: int = 5432
    DB_NAME: str = ''
    DATABASE_URL: str | None = None

    @property
    def db_url(self) -> str:
        if self.DATABASE_URL:
            return self.DATABASE_URL

        if not (self.DB_USER and self.DB_HOST and self.DB_NAME):
            return f"sqlite:///./{self.APP_NAME}.db"

        password_segment = f":{self.DB_PASSWORD}" if self.DB_PASSWORD else ""
        return (
            f"postgresql+psycopg://{self.DB_USER}{password_segment}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )


settings = Settings()
