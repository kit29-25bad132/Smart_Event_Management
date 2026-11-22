from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.dependencies import get_current_user, require_admin
from app.core.security import hash_password
from app.models import User
from app.schemas.common import UserOut
from app.schemas.user import UserUpdate
router = APIRouter(prefix="/api/users", tags=["users"])
@router.get("", response_model=list[UserOut])
def list_users(db: Session = Depends(get_db), _: User = Depends(require_admin)): return list(db.scalars(select(User).order_by(User.created_at)))
@router.get("/me", response_model=UserOut)
def profile(user=Depends(get_current_user)): return user
@router.patch("/me", response_model=UserOut)
def update_profile(data: UserUpdate, user=Depends(get_current_user), db: Session = Depends(get_db)):
    if data.email is not None: user.email = data.email.lower().strip()
    if data.password is not None: user.password_hash = hash_password(data.password)
    db.commit(); db.refresh(user); return user
