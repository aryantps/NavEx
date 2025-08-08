from fastapi import FastAPI
from sqlalchemy import inspect
from app.db.session import engine
from app.db.base_class import Base
from app.core.logger import logger


def register_startup_events(app: FastAPI):
    @app.on_event("startup")
    async def init_tables():
        logger.info("🔍 Inspecting database tables...")

        async with engine.begin() as conn:

            def sync_inspect(sync_conn):
                inspector = inspect(sync_conn)
                return inspector.get_table_names()

            tables = await conn.run_sync(sync_inspect)

            if tables:
                logger.info("✅ Tables already exist. Skipping creation.")
                log_table_list(tables)
            else:
                logger.info("⚙️  No tables found. Creating database schema...")
                await conn.run_sync(Base.metadata.create_all)
                tables = await conn.run_sync(sync_inspect)
                logger.info("✅ Tables created successfully.")
                log_table_list(tables)


def log_table_list(tables: list[str]):
    if not tables:
        logger.info("🚫 No tables found.")
        return

    table_log = "\n🗂️  Current Database Tables:\n" + "╔════════════════════════╗\n"
    for table in tables:
        table_log += f"║ 📦 {table.ljust(21)}║\n"
    table_log += "╚════════════════════════╝"
    logger.info(table_log)
