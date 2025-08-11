from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.core.config import get_settings

settings = get_settings()

engine = create_async_engine(
    settings.DATABASE_URL,
    pool_size=5, # persistent connections open to db
    max_overflow=10, # Extra temp conn open beyond pool_size when pool is full - not persistent
    pool_timeout=10, # wait in seconds to get a conn from pool before raising an error
    echo=False, # Set to True to log all SQL statements
    future=True
)


AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
