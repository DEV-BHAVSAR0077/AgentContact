from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.domain import ModelCreate, ModelResponse
from app.models.db import Model

router = APIRouter(prefix="/models", tags=["models"])

@router.post("/", response_model=ModelResponse)
def create_model(model_in: ModelCreate, db: Session = Depends(get_db)):
    db_model = Model(**model_in.model_dump())
    if db_model.api_key:
        # In a real app, encrypt this.
        pass
    db.add(db_model)
    db.commit()
    db.refresh(db_model)
    return db_model

@router.get("/", response_model=List[ModelResponse])
def get_models(db: Session = Depends(get_db)):
    return db.query(Model).all()

@router.get("/{model_id}", response_model=ModelResponse)
def get_model(model_id: str, db: Session = Depends(get_db)):
    db_model = db.query(Model).filter(Model.id == model_id).first()
    if not db_model:
        raise HTTPException(status_code=404, detail="Model not found")
    # Never return API keys
    db_model.api_key = "********" if db_model.api_key else None
    return db_model

@router.delete("/{model_id}")
def delete_model(model_id: str, db: Session = Depends(get_db)):
    db_model = db.query(Model).filter(Model.id == model_id).first()
    if not db_model:
        raise HTTPException(status_code=404, detail="Model not found")
    db.delete(db_model)
    db.commit()
    return {"message": "Model deleted"}

@router.post("/{model_id}/upload")
async def upload_model_file(model_id: str, file: UploadFile = File(...), db: Session = Depends(get_db)):
    db_model = db.query(Model).filter(Model.id == model_id).first()
    if not db_model:
        raise HTTPException(status_code=404, detail="Model not found")
    
    # In a real app, save to S3/Artifact storage and run validation
    db_model.file_name = file.filename
    db_model.status = "VALIDATING"
    db.commit()
    
    # Mocking validation completion for demo purposes
    db_model.status = "READY"
    db.commit()
    
    return {"message": "File uploaded and validation started", "status": db_model.status}
