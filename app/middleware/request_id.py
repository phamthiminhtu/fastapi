import uuid
from fastapi import FastAPI, Depends, Request, Response, Header, Query, HTTPException


async def request_id_middleware(request: Request, call_next):
    # 1. Generate or extract request ID
    # 2. Store in context variable
    # 3. Add to response headers
    request_id = request.headers.get("X-Request-ID")
    if not request_id:
        request_id = str(uuid.uuid4())
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response
