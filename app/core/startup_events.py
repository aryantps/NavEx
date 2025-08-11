from fastapi import FastAPI
from sqlalchemy import inspect
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager

from app.db.session import engine
from app.db.base_class import Base
from app.core.logger import logger
from app.core.seeder import run_seeders

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_tables_and_seed()
    yield

def log_table_list(tables: list[str]):
    if not tables:
        logger.info("🚫 No tables found.")
        return

    table_log = "\n🗂️  Current Database Tables:\n" + "╔════════════════════════╗\n"
    for table in tables:
        table_log += f"║ 📦 {table.ljust(21)}║\n"
    table_log += "╚════════════════════════╝"
    logger.info(table_log)

async def init_tables():
    logger.info("🔍 Inspecting database tables...")

    async with engine.begin() as conn:
        def sync_inspect(sync_conn):
            inspector = inspect(sync_conn)
            return set(inspector.get_table_names())

        existing_tables = await conn.run_sync(sync_inspect)
        defined_tables = set(Base.metadata.tables.keys())
        missing_tables = defined_tables - existing_tables

        if not missing_tables:
            logger.info("✅ All tables already exist. Skipping creation.")
        else:
            logger.info(f"⚙️  Missing tables detected: {', '.join(missing_tables)}")
            await conn.run_sync(Base.metadata.create_all)
            logger.info("✅ Missing tables created successfully.")

        all_tables = await conn.run_sync(sync_inspect)
        log_table_list(all_tables)

        logger.info("Seeding initial data...")
        async with AsyncSession(bind=conn) as session:
            await run_seeders(session)
        logger.info("Initial data seeded successfully.")

async def init_tables_and_seed():
    await init_tables()

    logger.info("Seeding initial data...")
    async with AsyncSession(bind=engine) as session:
        await run_seeders(session)
    logger.info("Initial data seeded successfully.")