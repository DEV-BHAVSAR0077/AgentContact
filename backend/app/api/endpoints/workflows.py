from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.domain import WorkflowCreate, WorkflowResponse, WorkflowBase
from app.models.db import Workflow

router = APIRouter(prefix="/workflows", tags=["workflows"])

@router.post("/", response_model=WorkflowResponse)
def create_workflow(workflow_in: WorkflowCreate, db: Session = Depends(get_db)):
    db_wf = Workflow(**workflow_in.model_dump())
    db.add(db_wf)
    db.commit()
    db.refresh(db_wf)
    return db_wf

@router.get("/", response_model=List[WorkflowResponse])
def get_workflows(db: Session = Depends(get_db)):
    return db.query(Workflow).all()

@router.get("/{wf_id}", response_model=WorkflowResponse)
def get_workflow(wf_id: str, db: Session = Depends(get_db)):
    db_wf = db.query(Workflow).filter(Workflow.id == wf_id).first()
    if not db_wf:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return db_wf

@router.put("/{wf_id}", response_model=WorkflowResponse)
def update_workflow(wf_id: str, workflow_in: WorkflowBase, db: Session = Depends(get_db)):
    db_wf = db.query(Workflow).filter(Workflow.id == wf_id).first()
    if not db_wf:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    update_data = workflow_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_wf, key, value)
        
    db.commit()
    db.refresh(db_wf)
    return db_wf

@router.delete("/{wf_id}")
def delete_workflow(wf_id: str, db: Session = Depends(get_db)):
    db_wf = db.query(Workflow).filter(Workflow.id == wf_id).first()
    if not db_wf:
        raise HTTPException(status_code=404, detail="Workflow not found")
    db.delete(db_wf)
    db.commit()
    return {"message": "Workflow deleted"}
