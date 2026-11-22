from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.dependencies import get_current_user
from app.schemas.auth import RegisterRequest, LoginRequest
from app.schemas.common import TokenResponse, UserOut
from app.services.auth_service import register, login
router = APIRouter(prefix="/api/auth", tags=["auth"])
@router.post("/register", response_model=TokenResponse, status_code=201)
def register_api(data: RegisterRequest, db: Session = Depends(get_db)):
    user, token = register(db, data.email, data.password); return {"access_token": token, "user": user}
@router.post("/login", response_model=TokenResponse)
def login_api(data: LoginRequest, db: Session = Depends(get_db)):
    user, token = login(db, data.email, data.password); return {"access_token": token, "user": user}
@router.get("/me", response_model=UserOut)
def me(user=Depends(get_current_user)): return user
