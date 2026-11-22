from uuid import UUID
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.dependencies import get_current_user, require_admin
from app.models import User, EventStatus
from app.schemas.event import EventCreate, EventUpdate, EventOut
from app.services import event_service
router = APIRouter(prefix="/api/events", tags=["events"])
@router.post("", response_model=EventOut, status_code=201)
def create(data: EventCreate, db: Session = Depends(get_db), user: User = Depends(require_admin)): return event_service.create(db, data, user.id)
@router.get("", response_model=list[EventOut])
def search(q: str | None = None, status: EventStatus | None = None, venue_id: UUID | None = None, page: int = Query(1, ge=1), page_size: int = Query(20, ge=1, le=100), db: Session = Depends(get_db)):
    items, _ = event_service.search(db, q, status, venue_id, page, page_size); return items
@router.get("/{event_id}", response_model=EventOut)
def get(event_id: UUID, db: Session = Depends(get_db)): return event_service.get(db, event_id)
@router.patch("/{event_id}", response_model=EventOut)
def update(event_id: UUID, data: EventUpdate, db: Session = Depends(get_db), _: User = Depends(require_admin)): return event_service.update(db, event_id, data)
@router.delete("/{event_id}", response_model=EventOut)
def cancel(event_id: UUID, db: Session = Depends(get_db), _: User = Depends(require_admin)): return event_service.cancel(db, event_id)
@router.post("/{event_id}/cancel", response_model=EventOut)
def cancel_compat(event_id: UUID, db: Session = Depends(get_db), _: User = Depends(require_admin)): return event_service.cancel(db, event_id)
