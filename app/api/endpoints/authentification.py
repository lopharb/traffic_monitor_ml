# auth_router.py

from fastapi import APIRouter, HTTPException, status
from ..schemas.auth import RegisterRequest, LoginRequest, TokenResponse
from ...services.database.db import DatabaseManager
from ...services.auth import create_access_token, verify_password

auth_router = APIRouter(prefix="/api/v1/auth")

db_manager = DatabaseManager()


@auth_router.post("/register")
async def register_user(request: RegisterRequest):
    if db_manager.get_user_by_username(request.username):
        raise HTTPException(status_code=400, detail="Username already exists")
    if db_manager.get_user_by_email(request.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    db_manager.create_user(
        username=request.username,
        email=request.email,
        password=request.password
    )
    return {"message": "User created successfully"}


@auth_router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest):
    user = db_manager.get_user_by_username(request.username)
    if not user or not verify_password(request.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid credentials",
                            headers={"WWW-Authenticate": "Bearer"})

    token = create_access_token(data={"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}
