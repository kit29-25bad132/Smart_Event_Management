from uuid import UUID
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models import Event, EventStatus, Venue

def _validate(db, data, current=None):
    incoming = data.model_dump(exclude_unset=True) if hasattr(data, "model_dump") else {}
    venue_id = incoming.get("venue_id", current.venue_id if current else None)
    venue = db.scalar(select(Venue).where(Venue.id == venue_id).with_for_update())
    if not venue or not venue.is_active: raise HTTPException(404, "Venue not found")
    values = incoming if current else data.model_dump()
    start = values.get("starts_at", current.starts_at if current else None); end = values.get("ends_at", current.ends_at if current else None); cap = values.get("capacity", current.capacity if current else None)
    if start >= end: raise HTTPException(422, "starts_at must be before ends_at")
    if cap > venue.capacity: raise HTTPException(422, "Event capacity exceeds venue capacity")
    conflicts = db.scalar(select(func.count()).select_from(Event).where(Event.venue_id == venue.id, Event.id != (current.id if current else None), Event.status.in_([EventStatus.DRAFT, EventStatus.PUBLISHED]), Event.starts_at < end, Event.ends_at > start))
    if conflicts: raise HTTPException(409, "Venue is already booked for this time")
    return venue
def create(db, data, creator_id):
    _validate(db, data); event = Event(**data.model_dump(), created_by=creator_id); db.add(event); db.commit(); db.refresh(event); return event
def search(db, q=None, status=None, venue_id=None, page=1, page_size=20):
    stmt = select(Event).where(Event.status == EventStatus.PUBLISHED)
    if q: stmt = stmt.where(Event.title.ilike(f"%{q}%"))
    if status: stmt = stmt.where(Event.status == status)
    if venue_id: stmt = stmt.where(Event.venue_id == venue_id)
    total = db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
    return list(db.scalars(stmt.order_by(Event.starts_at).offset((page-1)*page_size).limit(page_size))), total
def get(db, event_id):
    event = db.get(Event, event_id)
    if not event or event.status != EventStatus.PUBLISHED: raise HTTPException(404, "Event not found")
    return event
def update(db, event_id, data):
    event = get(db, event_id); payload = data.model_dump(exclude_unset=True)
    class Candidate: pass
    for key, value in payload.items(): setattr(event, key, value)
    _validate(db, event, event)
    db.commit(); db.refresh(event); return event
def cancel(db, event_id):
    event = get(db, event_id)
    if event.status == EventStatus.CANCELLED: raise HTTPException(409, "Event is already cancelled")
    event.status = EventStatus.CANCELLED; db.commit(); db.refresh(event); return event
