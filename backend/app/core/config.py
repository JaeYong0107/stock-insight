from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/stock_insight"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # KIS API (한국투자증권)
    KIS_APP_KEY: str = ""
    KIS_APP_SECRET: str = ""
    KIS_ACCOUNT_NO: str = ""

    # Claude API
    ANTHROPIC_API_KEY: str = ""

    class Config:
        env_file = ".env"


settings = Settings()
