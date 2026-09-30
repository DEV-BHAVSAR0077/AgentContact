from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import models, agents, workflows, executions, auth
from app.core.config import settings
import uuid
import time
import logging
from contextlib import asynccontextmanager
import redis.asyncio as redis
from fastapi_limiter import FastAPILimiter
import time
import logging

# Basic structured logger setup
logger = logging.getLogger("agentflow")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('{"time": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}'))
logger.addHandler(handler)

@asynccontextmanager
async def lifespan(app: FastAPI):
    redis_conn = redis.from_url(settings.REDIS_URL, encoding="utf-8", decode_responses=True)
    await FastAPILimiter.init(redis_conn)
    yield
    await redis_conn.close()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan
)

# CORS setup (Phase 1 Fix D8)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS if settings.CORS_ORIGINS else [],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_trace_and_log(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    request.state.request_id = request_id
    start_time = time.time()
    
    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        logger.info(f"Path: {request.url.path} | Method: {request.method} | Status: {response.status_code} | Duration: {process_time:.4f}s | ReqID: {request_id}")
        return response
    except Exception as exc:
        process_time = time.time() - start_time
        logger.error(f"Path: {request.url.path} | Error: {str(exc)} | Duration: {process_time:.4f}s | ReqID: {request_id}")
        return JSONResponse(
            status_code=500,
            content={
                "error": {
                    "code": "INTERNAL_SERVER_ERROR",
                    "message": "An unexpected error occurred.",
                    "request_id": request_id
                }
            }
        )

# Health endpoints
@app.get("/healthz", tags=["health"])
async def healthz():
    return {"status": "ok"}

@app.get("/readyz", tags=["health"])
async def readyz():
    # In future phases, verify DB and Redis connection here
    return {"status": "ready"}

# Includes routers
app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(models.router, prefix=settings.API_V1_STR)
app.include_router(agents.router, prefix=settings.API_V1_STR)
app.include_router(workflows.router, prefix=settings.API_V1_STR)
app.include_router(executions.router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    return {"message": "AgentFlow API is running"}
