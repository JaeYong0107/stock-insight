"""
애플리케이션 설정.

pydantic-settings를 사용하여 .env 파일과 환경 변수에서 설정값을 로딩한다.
settings 싱글턴 인스턴스를 통해 앱 전역에서 접근 가능하다.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

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


settings = Settings()
