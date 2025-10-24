
# learning-fastapi

A repo to familiarize myself with FastAPI framework and best practices. My teachers are Claude Code and Cursor.

### Key learning points

#### Key FastAPI components
Routers, Dependencies, Middleware, Models.

#### Authentication flow
```
Login 
-> Verify Password 
-> Create JWT 
-> Return Token

# 2 layers of protection: JWT and DB
Protected Request 
-> Decode JWT 
-> Check Cache 
-> Query DB (if needed) 
-> Verify Active 
-> Allow Access
```

#### JWT security
How JWT works, key points:
- Signature = HMAC_SHA256(Header + Payload, Secret_Key). How access token expiration works.
- Can't forge without server secret 
- Can't tamper without breaking signature 
- Expires automatically 

#### Caching strategy
```
Request 
-> Check Redis 
-> Cache Hit? Use it! (fast)
-> Cache Miss? Query DB 
-> Store in Redis (slower first time, fast after)
```
#### Environment configuration with Pydantic

Defaults in config.py -> Overridden by .env -> Overridden by system env vars -> Used via Pydantic settings object.

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

### Build an push docker image
- Script:
```
    ./scripts/build-and-push.sh
```
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

## Tests
- Get user access_token:
```
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=engineer&password=engineer123" 2>/dev/null
```
