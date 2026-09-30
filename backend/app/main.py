from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import models, agents, workflows, executions
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
)

from app.core.database import engine
from app.models.db import Base

Base.metadata.create_all(bind=engine)

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For dev only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Includes routers
app.include_router(models.router, prefix=settings.API_V1_STR)
app.include_router(agents.router, prefix=settings.API_V1_STR)
app.include_router(workflows.router, prefix=settings.API_V1_STR)
app.include_router(executions.router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    return {"message": "AgentFlow API is running"}
