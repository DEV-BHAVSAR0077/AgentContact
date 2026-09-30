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
async def execute_workflow(workflow_id: str, db: AsyncSession = Depends(get_db)):
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
    # For MVP, we simulate execution
    asyncio.create_task(simulate_execution(execution.id, db_wf.nodes, db_wf.edges))
    
    return execution

@router.get("/", response_model=list[ExecutionResponse])
async def get_executions(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Execution))
    return result.scalars().all()

@router.get("/{exec_id}", response_model=ExecutionResponse)
async def get_execution(exec_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Execution).where(Execution.id == exec_id))
    db_exec = result.scalars().first()
    if not db_exec:
        raise HTTPException(status_code=404, detail="Execution not found")
    return db_exec

@router.websocket("/{exec_id}/stream")
async def websocket_endpoint(websocket: WebSocket, exec_id: str):
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

async def simulate_execution(execution_id: str, nodes: List[Dict], edges: List[Dict]):
    # Mocking execution engine behavior
    for node in nodes:
        await asyncio.sleep(2)
        message = {
            "type": "log",
            "nodeId": node.get("id"),
            "status": "RUNNING",
            "message": f"Executing node {node.get('type', 'Unknown')}"
        }
        await broadcast_message(execution_id, message)
        
        await asyncio.sleep(2)
        message = {
            "type": "log",
            "nodeId": node.get("id"),
            "status": "COMPLETED",
            "message": f"Completed node {node.get('type', 'Unknown')}"
        }
        await broadcast_message(execution_id, message)
    
    # Update DB
    # We must construct a new session via async_sessionmaker
    # We can't import SessionLocal directly, we need to use the engine
    from app.core.database import engine
    SessionLocal = async_sessionmaker(engine, expire_on_commit=False)
    
    async with SessionLocal() as db:
        result = await db.execute(select(Execution).where(Execution.id == execution_id))
        execution = result.scalars().first()
        if execution:
            execution.status = "COMPLETED"
            execution.completed_at = datetime.now(timezone.utc)
            await db.commit()
            
            message = {
                "type": "status",
                "status": "COMPLETED"
            }
            await broadcast_message(execution_id, message)

async def broadcast_message(execution_id: str, message: dict):
    if execution_id in active_connections:
        websockets = active_connections[execution_id]
        for ws in websockets:
            try:
                await ws.send_json(message)
            except Exception:
                pass
