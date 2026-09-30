from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from typing import List, Dict, Any
import asyncio
import json
from app.core.database import get_db
from app.schemas.domain import ExecutionResponse
from app.models.db import Execution, Workflow
from datetime import datetime

router = APIRouter(prefix="/executions", tags=["executions"])

# Simple memory storage for active websockets
active_connections: Dict[str, List[WebSocket]] = {}

@router.post("/workflow/{workflow_id}", response_model=ExecutionResponse)
async def execute_workflow(workflow_id: str, db: Session = Depends(get_db)):
    db_wf = db.query(Workflow).filter(Workflow.id == workflow_id).first()
    if not db_wf:
        raise HTTPException(status_code=404, detail="Workflow not found")
        
    execution = Execution(workflow_id=workflow_id, status="RUNNING")
    db.add(execution)
    db.commit()
    db.refresh(execution)
    
    # In a real system, this would trigger a celery task or asyncio background task
    # For MVP, we simulate execution
    asyncio.create_task(simulate_execution(execution.id, db_wf.nodes, db_wf.edges))
    
    return execution

@router.get("/", response_model=List[ExecutionResponse])
def get_executions(db: Session = Depends(get_db)):
    return db.query(Execution).all()

@router.get("/{exec_id}", response_model=ExecutionResponse)
def get_execution(exec_id: str, db: Session = Depends(get_db)):
    db_exec = db.query(Execution).filter(Execution.id == exec_id).first()
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

async def simulate_execution(execution_id: str, nodes: List[Dict], edges: List[Dict]):
    # Mocking execution engine behavior
    for node in nodes:
        await asyncio.sleep(2)
        message = {
            "type": "log",
            "nodeId": node.get("id"),
            "status": "RUNNING",
            "message": f"Executing node {node.get('data', {}).get('label', 'Unknown')}"
        }
        await broadcast_message(execution_id, message)
        
        await asyncio.sleep(2)
        message = {
            "type": "log",
            "nodeId": node.get("id"),
            "status": "COMPLETED",
            "message": f"Completed node {node.get('data', {}).get('label', 'Unknown')}"
        }
        await broadcast_message(execution_id, message)
    
    # Update DB
    from app.core.database import SessionLocal
    db = SessionLocal()
    try:
        execution = db.query(Execution).filter(Execution.id == execution_id).first()
        if execution:
            execution.status = "COMPLETED"
            execution.completed_at = datetime.utcnow()
            db.commit()
            
            message = {
                "type": "status",
                "status": "COMPLETED"
            }
            await broadcast_message(execution_id, message)
    finally:
        db.close()

async def broadcast_message(execution_id: str, message: dict):
    if execution_id in active_connections:
        websockets = active_connections[execution_id]
        for ws in websockets:
            try:
                await ws.send_json(message)
            except Exception:
                pass
