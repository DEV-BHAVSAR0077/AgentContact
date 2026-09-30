from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy import create_engine, Column, String, Integer, DateTime, JSON, ForeignKey, Boolean
from datetime import datetime
import uuid

Base = declarative_base()

def generate_uuid():
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, default=generate_uuid)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class Model(Base):
    __tablename__ = "models"
    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, index=True)
    source_type = Column(String) # 'api' or 'uploaded'
    provider = Column(String, nullable=True) # e.g. openai, google
    model_name = Column(String, nullable=True) # e.g. gpt-4, gemini-pro
    api_key = Column(String, nullable=True)
    base_url = Column(String, nullable=True)
    temperature = Column(Integer, nullable=True)
    max_tokens = Column(Integer, nullable=True)
    system_prompt = Column(String, nullable=True)
    framework = Column(String, nullable=True) # for uploaded
    format = Column(String, nullable=True) # pkl, onnx
    file_name = Column(String, nullable=True)
    file_size = Column(Integer, nullable=True)
    status = Column(String, default="READY")
    input_schema = Column(JSON, nullable=True)
    output_schema = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
class Agent(Base):
    __tablename__ = "agents"
    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String)
    description = Column(String, nullable=True)
    model_id = Column(String, ForeignKey("models.id"))
    system_prompt = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Workflow(Base):
    __tablename__ = "workflows"
    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String)
    description = Column(String, nullable=True)
    nodes = Column(JSON, default=list) # Store react-flow nodes
    edges = Column(JSON, default=list) # Store react-flow edges
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Execution(Base):
    __tablename__ = "executions"
    id = Column(String, primary_key=True, default=generate_uuid)
    workflow_id = Column(String, ForeignKey("workflows.id"))
    status = Column(String, default="PENDING") # PENDING, RUNNING, COMPLETED, FAILED
    result = Column(JSON, nullable=True)
    error = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
