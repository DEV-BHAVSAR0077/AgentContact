from pydantic import BaseModel, Field, ConfigDict
from typing import Literal, Union, Annotated, Any
from datetime import datetime

class ModelBase(BaseModel):
    name: str
    source_type: str
    provider: str | None = None
    model_name: str | None = None
    api_key: str | None = None
    base_url: str | None = None
    temperature: float | None = None
    max_tokens: int | None = None
    system_prompt: str | None = None
    framework: str | None = None
    format: str | None = None
    input_schema: dict[str, Any] | None = None
    output_schema: dict[str, Any] | None = None

class ModelCreate(ModelBase):
    pass

class ModelResponse(ModelBase):
    id: str
    status: str
    file_name: str | None = None
    file_size: int | None = None
    error: str | None = None
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class AgentBase(BaseModel):
    name: str
    description: str | None = None
    model_id: str
    system_prompt: str | None = None

class AgentCreate(AgentBase):
    pass

class AgentResponse(AgentBase):
    id: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

# Graph schemas (ADR 0002)

class AgentNode(BaseModel):
    id: str
    type: Literal["agent"]
    agent_id: str
    prompt_override: str | None = None

class ModelNode(BaseModel):
    id: str
    type: Literal["model"]
    model_id: str

class ToolNode(BaseModel):
    id: str
    type: Literal["tool"]
    tool_name: str

WorkflowNode = Annotated[Union[AgentNode, ModelNode, ToolNode], Field(discriminator="type")]

class Edge(BaseModel):
    id: str
    source: str
    target: str
    source_handle: str | None = None
    target_handle: str | None = None

class WorkflowBase(BaseModel):
    name: str
    description: str | None = None
    nodes: list[WorkflowNode] = Field(default_factory=list)
    edges: list[Edge] = Field(default_factory=list)

class WorkflowCreate(WorkflowBase):
    pass

class WorkflowResponse(WorkflowBase):
    id: str
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

class ExecutionResponse(BaseModel):
    id: str
    workflow_id: str | None = None
    workflow_snapshot: dict[str, Any] | None = None
    status: str
    result: dict[str, Any] | None = None
    error: str | None = None
    created_at: datetime
    completed_at: datetime | None = None
    model_config = ConfigDict(from_attributes=True)
