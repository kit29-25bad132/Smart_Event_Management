from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models import Venue, Event, EventStatus

def create(db: Session, data):
    venue = Venue(**data.model_dump()); db.add(venue); db.commit(); db.refresh(venue); return venue
def list_active(db: Session): return list(db.scalars(select(Venue).where(Venue.is_active.is_(True)).order_by(Venue.name)))
def get(db: Session, venue_id: UUID):
    venue = db.get(Venue, venue_id)
    if not venue: raise HTTPException(404, "Venue not found")
    return venue
def update(db: Session, venue_id: UUID, data):
    venue = get(db, venue_id)
    for key, value in data.model_dump(exclude_unset=True).items(): setattr(venue, key, value)
    db.commit(); db.refresh(venue); return venue
def availability(db: Session, venue_id: UUID, starts_at, ends_at):
    get(db, venue_id)
    conflicts = list(db.scalars(select(Event).where(Event.venue_id == venue_id, Event.status.in_([EventStatus.DRAFT, EventStatus.PUBLISHED]), Event.starts_at < ends_at, Event.ends_at > starts_at)))
    return {"available": not conflicts, "conflicts": conflicts}
