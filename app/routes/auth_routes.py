from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas import (
    RegisterRequest,
    LoginRequest,
    TokenResponse,
    MessageResponse
)
from app.models import User
from app.dependencies import get_db
from app.utils.security import hash_password, verify_password
from app.auth import create_access_token

router = APIRouter()

@router.post(
    "/register",
    response_model=MessageResponse,
    status_code=201
)
def register(data: RegisterRequest, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(
        User.email == data.email
    ).first()

    if existing_user:
        raise HTTPException(400, "Email already exists")

    user = User(
        email=data.email,
        hashed_password=hash_password(data.password)
    )

    db.add(user)
    db.commit()

    return {"message": "User created successfully"}


@router.post(
    "/login",
    response_model=TokenResponse
)
def login(data: LoginRequest, db: Session = Depends(get_db)):

    user = db.query(User).filter(
        User.email == data.email
    ).first()

    if not user:
        raise HTTPException(401, "Invalid email or password")

    if not verify_password(data.password, user.hashed_password):
        raise HTTPException(401, "Invalid email or password")

    token = create_access_token({
        "user_id": user.id
    })

    return {
        "access_token": token
    }