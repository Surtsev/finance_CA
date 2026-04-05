from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from src.config import settings
from src.entity.repositories.mark_repository import MarkRepository
from src.infra.adapters.redis_cache import CacheService
from src.infra.adapters.redis_client import redis_client
from src.infra.adapters.sqlalchemy_mark_repository import SQLAlchemyMarkRepository
from src.infra.gateways.mark_gateway import CachedMarkGateway


engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    future=True,
)

async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


@asynccontextmanager
async def lifespan(app):
    """Application lifespan: manage Redis connections."""
    await redis_client.connect()
    yield
    await redis_client.disconnect()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency для получения сессии БД."""
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def get_cached_mark_repository(
    session: AsyncSession,
) -> MarkRepository:
    """Dependency: cached MarkRepository with Redis cache-aside.

    Usage in FastAPI:
        @router.get("/marks/{name}")
        async def get_mark(repo: MarkRepository = Depends(get_cached_mark_repository)):
            return await repo.get_by_name(name)
    """
    base_repo = SQLAlchemyMarkRepository(session)
    cache = CacheService(redis_client)
    return CachedMarkGateway(base_repo, cache)


async def get_mark_repository(session: AsyncSession) -> MarkRepository:
    """Dependency: pure SQLAlchemy MarkRepository without caching.

    Usage when you need direct DB access (e.g., tests, admin operations).
    """
    return SQLAlchemyMarkRepository(session)
