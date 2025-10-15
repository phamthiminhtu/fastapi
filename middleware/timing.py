import uuid
import time
import logging
from fastapi import FastAPI, Depends, Request, Response, Header, Query, HTTPException

SLOW_REQUEST_THRESHOLD = 1.0
logger = logging.getLogger(__name__)

async def timing_middleware(request: Request, call_next):
    """
    Measure request processing time.
    
    - Records start time
    - Adds X-Response-Time header (in milliseconds)
    - Logs warning for slow requests
    """
    start_time = time.time()
    
    response = await call_next(request)
    
    duration = time.time() - start_time
    duration_ms = duration * 1000
    
    response.headers['X-Response-Time'] = f"{duration_ms:.2f}ms"
    
    # Log slow requests
    if duration > SLOW_REQUEST_THRESHOLD:
        logger.warning(
            f"Slow request: {request.method} {request.url.path} "
            f"took {duration:.3f}s"
        )
    
    return response