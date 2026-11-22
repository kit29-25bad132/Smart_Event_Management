from datetime import datetime
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.dependencies import require_admin, get_current_user
from app.schemas.venue import VenueCreate, VenueUpdate, VenueOut
from app.services import venue_service
router = APIRouter(prefix="/api/venues", tags=["venues"])
@router.post("", response_model=VenueOut, status_code=201)
def create(data: VenueCreate, db: Session = Depends(get_db), _: object = Depends(require_admin)): return venue_service.create(db, data)
@router.get("", response_model=list[VenueOut])
def list_venues(db: Session = Depends(get_db), _: object = Depends(get_current_user)): return venue_service.list_active(db)
@router.get("/{venue_id}", response_model=VenueOut)
def get(venue_id, db: Session = Depends(get_db), _: object = Depends(get_current_user)): return venue_service.get(db, venue_id)
@router.patch("/{venue_id}", response_model=VenueOut)
def update(venue_id, data: VenueUpdate, db: Session = Depends(get_db), _: object = Depends(require_admin)): return venue_service.update(db, venue_id, data)
@router.get("/{venue_id}/availability")
def avail(venue_id, starts_at: datetime = Query(...), ends_at: datetime = Query(...), db: Session = Depends(get_db), _: object = Depends(get_current_user)):
    if starts_at >= ends_at: from fastapi import HTTPException; raise HTTPException(422, "Invalid time range")
    result = venue_service.availability(db, venue_id, starts_at, ends_at); result["conflicts"] = [{"id": e.id, "title": e.title, "starts_at": e.starts_at, "ends_at": e.ends_at} for e in result["conflicts"]]; return result
