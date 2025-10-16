
# fastapi
A repo to familiarize myself with FastAPI framework and best practices


## Dockerize
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
