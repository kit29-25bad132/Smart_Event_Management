from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.dependencies import get_current_user, require_admin
from app.models import User
from app.schemas.registration import RegistrationOut
from app.services import registration_service
router = APIRouter(prefix="/api", tags=["registrations"])
@router.post("/events/{event_id}/register", response_model=RegistrationOut, status_code=201)
def register(event_id: UUID, db: Session = Depends(get_db), user: User = Depends(get_current_user)): return registration_service.register(db, event_id, user)
@router.delete("/events/{event_id}/register", response_model=RegistrationOut)
def cancel(event_id: UUID, db: Session = Depends(get_db), user: User = Depends(get_current_user)): return registration_service.cancel(db, event_id, user)
@router.get("/registrations/me", response_model=list[RegistrationOut])
def mine(db: Session = Depends(get_db), user: User = Depends(get_current_user)): return registration_service.mine(db, user.id)
@router.get("/events/{event_id}/registrations", response_model=list[RegistrationOut])
def event_registrations(event_id: UUID, db: Session = Depends(get_db), _: User = Depends(require_admin)): return registration_service.for_event(db, event_id)
