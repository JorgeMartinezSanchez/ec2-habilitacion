from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from src.core.config import settings
from src.db.base import Base

engine = create_async_engine(
    settings.database_url,
    pool_pre_ping=True,
    echo=False
)

_session_factory = async_sessionmaker(engine, expire_on_commit=False)

async def get_db_session() -> AsyncSession:
    async with _session_factory() as session:
        yield session