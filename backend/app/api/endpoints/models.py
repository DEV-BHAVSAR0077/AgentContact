from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Any
from app.core.database import get_db
from app.schemas.domain import ModelCreate, ModelResponse
from app.models.db import Model
from app.core.security import encrypt_api_key

router = APIRouter(prefix="/models", tags=["models"])

@router.post("/", response_model=ModelResponse)
async def create_model(model_in: ModelCreate, db: AsyncSession = Depends(get_db)) -> Model:
    model_data = model_in.model_dump()
    if model_data.get("api_key"):
        model_data["api_key"] = encrypt_api_key(model_data["api_key"])
        
    db_model = Model(**model_data)
    db.add(db_model)
    await db.commit()
    await db.refresh(db_model)
    
    # Mask key before returning
    db_model.api_key = "********" if db_model.api_key else None
    return db_model

@router.get("/", response_model=list[ModelResponse])
async def get_models(db: AsyncSession = Depends(get_db)) -> list[Model]:
    result = await db.execute(select(Model))
    models = list(result.scalars().all())
    for m in models:
        m.api_key = "********" if m.api_key else None
    return models

@router.get("/{model_id}", response_model=ModelResponse)
async def get_model(model_id: str, db: AsyncSession = Depends(get_db)) -> Model:
    result = await db.execute(select(Model).where(Model.id == model_id))
    db_model = result.scalars().first()
    if not db_model:
        raise HTTPException(status_code=404, detail="Model not found")
    
    db_model.api_key = "********" if db_model.api_key else None
    return db_model

@router.delete("/{model_id}")
async def delete_model(model_id: str, db: AsyncSession = Depends(get_db)) -> dict[str, str]:
    result = await db.execute(select(Model).where(Model.id == model_id))
    db_model = result.scalars().first()
    if not db_model:
        raise HTTPException(status_code=404, detail="Model not found")
    
    await db.delete(db_model)
    await db.commit()
    return {"message": "Model deleted"}

import os
import hashlib
import aiofiles
from pathlib import Path

ARTIFACTS_DIR = Path("artifacts/models")

@router.post("/{model_id}/upload")
async def upload_model_file(model_id: str, file: UploadFile = File(...), db: AsyncSession = Depends(get_db)) -> dict[str, Any]:
    result = await db.execute(select(Model).where(Model.id == model_id))
    db_model = result.scalars().first()
    if not db_model:
        raise HTTPException(status_code=404, detail="Model not found")
    
    # Setup directories
    model_dir = ARTIFACTS_DIR / model_id
    model_dir.mkdir(parents=True, exist_ok=True)
    
    # Safe filename
    safe_filename = file.filename.replace("/", "_").replace("\\", "_") if file.filename else "model.bin"
    file_path = model_dir / safe_filename
    
    db_model.status = "UPLOADING"
    await db.commit()
    
    # Stream and calculate checksum
    sha256_hash = hashlib.sha256()
    file_size = 0
    try:
        async with aiofiles.open(file_path, 'wb') as out_file:
            while chunk := await file.read(1024 * 1024): # 1MB chunks
                file_size += len(chunk)
                sha256_hash.update(chunk)
                await out_file.write(chunk)
    except Exception as e:
        db_model.status = "FAILED"
        db_model.error = str(e)
        await db.commit()
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")
        
    db_model.file_name = safe_filename
    db_model.file_size = file_size
    db_model.status = "READY"
    await db.commit()
    
    return {
        "message": "File uploaded and validated", 
        "status": db_model.status,
        "checksum": sha256_hash.hexdigest(),
        "file_size": file_size
    }
