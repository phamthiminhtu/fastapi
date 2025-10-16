
# fastapi
A repo to familiarize myself with FastAPI framework and best practices

### Local development with Docker 

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

### Build local Docker image
- CLI:
```
    docker build -t fastapi-app:latest ~/workspace/fast-api-app
    docker tag fastapi-app:latest tototus/fastapi-app:latest
    docker push tototus/fastapi-app:latest
```

## Run in venv
```
uvicorn main:app --reload
```
