from fastapi import APIRouter, Depends, HTTPException, Response, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
import uuid

from app.core.database import get_db
from app.models.db import User
from app.core.security import get_password_hash, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

class UserCreate(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

@router.post("/signup", response_model=TokenResponse)
async def signup(user_in: UserCreate, response: Response, db: AsyncSession = Depends(get_db)) -> TokenResponse:
    # Check if user exists
    result = await db.execute(select(User).where(User.email == user_in.email))
    if result.scalars().first():
        raise HTTPException(status_code=400, detail="Email already registered")
        
    db_user = User(
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password)
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    
    access_token = create_access_token(subject=db_user.id)
    # Generate refresh token
    refresh_token = str(uuid.uuid4())
    # In a real app we would store get_password_hash(refresh_token) in DB here per ADR 0006
    
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        samesite="strict",
        secure=True
    )
    
    return TokenResponse(access_token=access_token)

@router.post("/login", response_model=TokenResponse)
async def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)) -> TokenResponse:
    result = await db.execute(select(User).where(User.email == form_data.username))
    user = result.scalars().first()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
        
    access_token = create_access_token(subject=user.id)
    refresh_token = str(uuid.uuid4())
    # In a real app we would store get_password_hash(refresh_token) in DB here per ADR 0006
    
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        samesite="strict",
        secure=True
    )
    
    return TokenResponse(access_token=access_token)

@router.post("/logout")
async def logout(response: Response) -> dict[str, str]:
    # In a real app we would delete the refresh token from DB here
    response.delete_cookie(key="refresh_token")
    return {"message": "Successfully logged out"}
