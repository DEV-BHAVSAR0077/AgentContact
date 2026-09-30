from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from app.core.database import get_db
from app.schemas.domain import WorkflowCreate, WorkflowResponse, WorkflowBase
from app.models.db import Workflow

router = APIRouter(prefix="/workflows", tags=["workflows"])

@router.post("/", response_model=WorkflowResponse)
async def create_workflow(workflow_in: WorkflowCreate, db: AsyncSession = Depends(get_db)):
    db_wf = Workflow(**workflow_in.model_dump())
    db.add(db_wf)
    await db.commit()
    await db.refresh(db_wf)
    return db_wf

@router.get("/", response_model=list[WorkflowResponse])
async def get_workflows(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Workflow))
    return result.scalars().all()

@router.get("/{wf_id}", response_model=WorkflowResponse)
async def get_workflow(wf_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Workflow).where(Workflow.id == wf_id))
    db_wf = result.scalars().first()
    if not db_wf:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return db_wf

@router.put("/{wf_id}", response_model=WorkflowResponse)
async def update_workflow(wf_id: str, workflow_in: WorkflowBase, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Workflow).where(Workflow.id == wf_id))
    db_wf = result.scalars().first()
    if not db_wf:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    # Store nodes and edges strictly using model dump to canonical schema format
    # The pydantic model WorkflowBase already validated them
    update_data = workflow_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_wf, key, value)
        
    await db.commit()
    await db.refresh(db_wf)
    return db_wf

@router.delete("/{wf_id}")
async def delete_workflow(wf_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Workflow).where(Workflow.id == wf_id))
    db_wf = result.scalars().first()
    if not db_wf:
        raise HTTPException(status_code=404, detail="Workflow not found")
    await db.delete(db_wf)
    await db.commit()
    return {"message": "Workflow deleted"}
