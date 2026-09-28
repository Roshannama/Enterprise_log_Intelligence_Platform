from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.auth.dependencies import require_admin
from app.auth.schemas import LoginRequest, RegisterRequest, TokenResponse, UserResponse
from app.auth.service import authenticate_user, create_user
from app.db.database import get_db

router = APIRouter(prefix="/api/auth", tags=["authentication"])
@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    return authenticate_user(
        db=db, username=request.username, password=request.password
    )
@router.post("/register", response_model=UserResponse)
def register(
    request: RegisterRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_admin),
):
    return create_user(
        db=db,
        username=request.username,
        email=request.email,
        full_name=request.full_name,
        password=request.password,
        role=request.role,
        department=request.department,
    )
