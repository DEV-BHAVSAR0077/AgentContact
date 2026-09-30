from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from app.core.database import get_db
from app.schemas.domain import ModelCreate, ModelResponse
from app.models.db import Model
from app.core.security import encrypt_api_key

router = APIRouter(prefix="/models", tags=["models"])

@router.post("/", response_model=ModelResponse)
async def create_model(model_in: ModelCreate, db: AsyncSession = Depends(get_db)):
    db_model = Model(**model_in.model_dump())
    if db_model.api_key:
        db_model.api_key = encrypt_api_key(db_model.api_key)
    db.add(db_model)
    await db.commit()
    await db.refresh(db_model)
    
    # Mask key before returning
    db_model.api_key = "********" if db_model.api_key else None
    return db_model

@router.get("/", response_model=list[ModelResponse])
async def get_models(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Model))
    models = result.scalars().all()
    for m in models:
        m.api_key = "********" if m.api_key else None
    return models

@router.get("/{model_id}", response_model=ModelResponse)
async def get_model(model_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Model).where(Model.id == model_id))
    db_model = result.scalars().first()
    if not db_model:
        raise HTTPException(status_code=404, detail="Model not found")
    
    db_model.api_key = "********" if db_model.api_key else None
    return db_model

@router.delete("/{model_id}")
async def delete_model(model_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Model).where(Model.id == model_id))
    db_model = result.scalars().first()
    if not db_model:
        raise HTTPException(status_code=404, detail="Model not found")
    
    await db.delete(db_model)
    await db.commit()
    return {"message": "Model deleted"}

@router.post("/{model_id}/upload")
async def upload_model_file(model_id: str, file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Model).where(Model.id == model_id))
    db_model = result.scalars().first()
    if not db_model:
        raise HTTPException(status_code=404, detail="Model not found")
    
    # In a real app, save to S3/Artifact storage and run validation
    db_model.file_name = file.filename
    db_model.status = "VALIDATING"
    await db.commit()
    
    # Mocking validation completion for demo purposes
    db_model.status = "READY"
    await db.commit()
    
    return {"message": "File uploaded and validation started", "status": db_model.status}
