from datetime import datetime
from fastapi import HTTPException
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.auth.jwt import create_access_token
from app.db.models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return pwd_context.verify(password, password_hash)


def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid username or password.")
    if not user.is_active:
        raise HTTPException(status_code=403, detail="User account is inactive.")
    if not verify_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid username or password.")
    user.last_login = datetime.utcnow()
    db.commit()
    token = create_access_token(
        {"sub": user.username, "user_id": user.id, "role": user.role}
    )
    return {
        "access_token": token,
        "token_type": "bearer",
        "username": user.username,
        "role": user.role,
        "user_id": user.id,
    }


def create_user(
    db: Session,
    username: str,
    email: str,
    full_name: str,
    password: str,
    role: str,
    department: str | None,
):
    if db.query(User).filter(User.username == username).first():
        raise HTTPException(status_code=400, detail="Username already exists.")
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(status_code=400, detail="Email already exists.")
    allowed_roles = {"admin", "analyst", "viewer"}
    if role not in allowed_roles:
        raise HTTPException(status_code=400, detail="Invalid role.")
    user = User(
        username=username,
        email=email,
        full_name=full_name,
        password_hash=hash_password(password),
        role=role,
        department=department,
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
