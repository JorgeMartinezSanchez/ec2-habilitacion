import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from src.core.config import settings
from src.main import app
from src.db.postgres import get_db_session

@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"

@pytest.fixture(scope="session")
async def engine():
    engine = create_async_engine(settings.database_url, pool_pre_ping=True)
    yield engine
    await engine.dispose()

@pytest.fixture
async def db_session(engine):
    async with engine.connect() as connection:
        async with connection.begin() as transaction:
            session = AsyncSession(bind=connection, expire_on_commit=False)
            yield session
            await session.close()
            await transaction.rollback()

@pytest.fixture(autouse=True)
def override_db(db_session):
    app.dependency_overrides.clear()
    async def _override():
        yield db_session
    app.dependency_overrides[get_db_session] = _override
    yield
    app.dependency_overrides.clear()