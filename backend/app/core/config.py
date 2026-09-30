import os
from typing import List, Union
from pydantic import AnyHttpUrl, field_validator, ValidationInfo
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "AgentFlow"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    ENV: str = "development"
    
    # Secrets - No defaults in production!
    SECRET_KEY: str
    ENCRYPTION_MASTER_KEY: str
    
    # CORS
    CORS_ORIGINS: Union[List[str], str] = []

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    # Database
    DATABASE_URL: str
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True, extra="ignore")

    @field_validator("SECRET_KEY", "ENCRYPTION_MASTER_KEY", mode="after")
    @classmethod
    def check_secrets(cls, v: str, info) -> str:
        if v in ("", "placeholder", "changeme") or len(v) < 16:
            # We allow tests to bypass this if strictly needed, but production MUST fail
            if os.getenv("ENV", "development") == "production":
                raise ValueError(f"{info.field_name} must be properly set in production (minimum 16 chars).")
        return v
    
    @field_validator("DATABASE_URL", mode="after")
    @classmethod
    def check_database_url(cls, v: str, info) -> str:
        if os.getenv("ENV", "development") == "production":
            if "sqlite" in v:
                raise ValueError("SQLite is not allowed in production. Use PostgreSQL.")
        return v

settings = Settings()
