from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class ModelBase(BaseModel):
    name: str
    source_type: str
    provider: Optional[str] = None
    model_name: Optional[str] = None
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None
    system_prompt: Optional[str] = None
    framework: Optional[str] = None
    format: Optional[str] = None
    input_schema: Optional[Dict[str, Any]] = None
    output_schema: Optional[Dict[str, Any]] = None

class ModelCreate(ModelBase):
    pass

class ModelResponse(ModelBase):
    id: str
    status: str
    file_name: Optional[str] = None
    file_size: Optional[int] = None
    created_at: datetime
    class Config:
        orm_mode = True

class AgentBase(BaseModel):
    name: str
    description: Optional[str] = None
    model_id: str
    system_prompt: Optional[str] = None

class AgentCreate(AgentBase):
    pass

class AgentResponse(AgentBase):
    id: str
    created_at: datetime
    class Config:
        orm_mode = True

class WorkflowBase(BaseModel):
    name: str
    description: Optional[str] = None
    nodes: List[Dict[str, Any]] = []
    edges: List[Dict[str, Any]] = []

class WorkflowCreate(WorkflowBase):
    pass

class WorkflowResponse(WorkflowBase):
    id: str
    created_at: datetime
    updated_at: datetime
    class Config:
        orm_mode = True

class ExecutionResponse(BaseModel):
    id: str
    workflow_id: str
    status: str
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    created_at: datetime
    completed_at: Optional[datetime] = None
    class Config:
        orm_mode = True
