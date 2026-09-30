from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "AgentFlow"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "agentflow"
    POSTGRES_PASSWORD: str = "agentflow_password"
    POSTGRES_DB: str = "agentflow_db"
    
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    
    SECRET_KEY: str = "super_secret_key_for_agentflow"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return f"sqlite:///./agentflow.db"

settings = Settings()
