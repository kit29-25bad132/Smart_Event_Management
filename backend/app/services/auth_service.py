from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models import User, UserRole
from app.core.security import hash_password, verify_password, create_access_token

def register(db: Session, email: str, password: str):
    email = email.lower().strip()
    if db.scalar(select(User).where(User.email == email)): raise HTTPException(409, "Email is already registered")
    user = User(email=email, password_hash=hash_password(password), role=UserRole.USER)
    db.add(user); db.commit(); db.refresh(user)
    return user, create_access_token(user.id, user.role.value)

def login(db: Session, email: str, password: str):
    user = db.scalar(select(User).where(User.email == email.lower().strip()))
    if not user or not verify_password(password, user.password_hash): raise HTTPException(401, "Invalid email or password")
    return user, create_access_token(user.id, user.role.value)
