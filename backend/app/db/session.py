"""
비동기 DB 엔진 및 세션 팩토리.

- engine: asyncpg 기반 async SQLAlchemy 엔진.
- async_session_factory: 요청마다 독립적인 AsyncSession을 생성하는 팩토리.
- get_db: FastAPI dependency로 사용하여 요청 스코프 세션을 제공한다.
"""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
)

async_session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency that yields an async DB session."""
    async with async_session_factory() as session:
        yield session
