#!/usr/bin/env python3
"""Seed database with sample data"""

import asyncio
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.core.config import settings
from app.models.db_models import Pipeline, User
from app.models.schemas import PipelineStatus


async def seed_data():
    """Seed the database with sample data"""

    # Create engine
    engine = create_async_engine(settings.database_url, echo=True)

    # Create session
    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        print("Seeding pipelines...")

        pipelines = [
            Pipeline(
                name="customer_etl",
                status=PipelineStatus.RUNNING,
                created_at=datetime.now() - timedelta(days=30),
                last_run=datetime.now() - timedelta(hours=2),
                success_rate=98.5,
                records_processed=150000,
                tags=["customer", "daily", "etl"]
            ),
            Pipeline(
                name="sales_analytics",
                status=PipelineStatus.STOPPED,
                created_at=datetime.now() - timedelta(days=25),
                last_run=datetime.now() - timedelta(hours=5),
                success_rate=95.2,
                records_processed=89000,
                tags=["sales", "hourly", "analytics"]
            ),
            Pipeline(
                name="inventory_sync",
                status=PipelineStatus.RUNNING,
                created_at=datetime.now() - timedelta(days=20),
                last_run=datetime.now() - timedelta(minutes=30),
                success_rate=99.1,
                records_processed=45000,
                tags=["inventory", "realtime"]
            ),
        ]

        for pipeline in pipelines:
            session.add(pipeline)

        print("Seeding users...")

        users = [
            User(
                username="admin",
                email="admin@example.com",
                hashed_password="hashed_admin_password",  # In production, use proper password hashing
                role="admin",
                is_active=1
            ),
            User(
                username="engineer",
                email="engineer@example.com",
                hashed_password="hashed_engineer_password",
                role="data_engineer",
                is_active=1
            ),
            User(
                username="user",
                email="user@example.com",
                hashed_password="hashed_user_password",
                role="user",
                is_active=1
            ),
        ]

        for user in users:
            session.add(user)

        await session.commit()
        print("✅ Database seeded successfully!")

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(seed_data())
