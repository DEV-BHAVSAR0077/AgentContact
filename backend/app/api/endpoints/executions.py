from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Dict, Any
import asyncio
from app.core.database import get_db, async_sessionmaker
from app.schemas.domain import ExecutionResponse
from app.models.db import Execution, Workflow
from datetime import datetime, timezone

router = APIRouter(prefix="/executions", tags=["executions"])

# Simple memory storage for active websockets
active_connections: Dict[str, List[WebSocket]] = {}

@router.post("/workflow/{workflow_id}", response_model=ExecutionResponse)
async def execute_workflow(workflow_id: str, db: AsyncSession = Depends(get_db)) -> Execution:
    result = await db.execute(select(Workflow).where(Workflow.id == workflow_id))
    db_wf = result.scalars().first()
    if not db_wf:
        raise HTTPException(status_code=404, detail="Workflow not found")
        
    # Phase 3 feature: Store workflow snapshot at execution time
    workflow_snapshot = {
        "nodes": db_wf.nodes,
        "edges": db_wf.edges
    }
    
    execution = Execution(
        workflow_id=workflow_id, 
        status="RUNNING",
        workflow_snapshot=workflow_snapshot
    )
    db.add(execution)
    await db.commit()
    await db.refresh(execution)
    
    # In a real system, this would trigger a celery task or asyncio background task
    asyncio.create_task(execute_in_background(execution.id, db_wf.nodes, db_wf.edges))
    
    return execution

@router.get("/", response_model=list[ExecutionResponse])
async def get_executions(db: AsyncSession = Depends(get_db)) -> list[Execution]:
    result = await db.execute(select(Execution))
    return list(result.scalars().all())

@router.get("/{exec_id}", response_model=ExecutionResponse)
async def get_execution(exec_id: str, db: AsyncSession = Depends(get_db)) -> Execution:
    result = await db.execute(select(Execution).where(Execution.id == exec_id))
    db_exec = result.scalars().first()
    if not db_exec:
        raise HTTPException(status_code=404, detail="Execution not found")
    return db_exec

@router.websocket("/{exec_id}/stream")
async def websocket_endpoint(websocket: WebSocket, exec_id: str, token: str | None = None) -> None:
    # In a real app, validate the token against the DB/JWT secret
    if not token:
        await websocket.close(code=1008, reason="Missing authentication token")
        return
        
    await websocket.accept()
    if exec_id not in active_connections:
        active_connections[exec_id] = []
    active_connections[exec_id].append(websocket)
    try:
        while True:
            # Just keep the connection open
            await websocket.receive_text()
    except WebSocketDisconnect:
        active_connections[exec_id].remove(websocket)
        if not active_connections[exec_id]:
            del active_connections[exec_id]

from app.core.engine import GraphEngine

async def execute_in_background(execution_id: str, nodes: List[Dict[str, Any]], edges: List[Dict[str, Any]]) -> None:
    engine = GraphEngine(execution_id, nodes, edges, broadcast_message)
    await engine.run()

async def broadcast_message(execution_id: str, message: dict[str, Any]) -> None:
    if execution_id in active_connections:
        websockets = active_connections[execution_id]
        for ws in websockets:
            try:
                await ws.send_json(message)
            except Exception:
                pass
