# Database Integration Guide

## Overview

This FastAPI application now uses **PostgreSQL** with **SQLAlchemy 2.0** (async) and **Alembic** for migrations.

## Database Setup

### Using Docker (Recommended)

1. **Start the application with database:**
   ```bash
   docker-compose up -d
   ```

   This will:
   - Start PostgreSQL container
   - Start FastAPI application
   - Wait for database to be healthy before starting the app

2. **Create initial migration:**
   ```bash
   # Inside the API container or locally with DB access
   alembic revision --autogenerate -m "Initial migration"
   alembic upgrade head
   ```

3. **Seed sample data:**
   ```bash
   python scripts/seed_data.py
   ```

### Local Development

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment:**
   Create a `.env` file (use `.env.example` as template):
   ```bash
   cp .env.example .env
   ```

3. **Start PostgreSQL:**
   ```bash
   docker-compose up db -d
   ```

4. **Run migrations:**
   ```bash
   alembic upgrade head
   ```

5. **Seed data:**
   ```bash
   python scripts/seed_data.py
   ```

6. **Start the application:**
   ```bash
   uvicorn main:app --reload
   ```