from datetime import datetime, timezone
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models import Event, EventStatus, Registration, RegistrationStatus, User

def register(db: Session, event_id, user: User):
    event = db.scalar(select(Event).where(Event.id == event_id).with_for_update())
    if not event: raise HTTPException(404, "Event not found")
    if event.status != EventStatus.PUBLISHED or event.ends_at <= datetime.now(timezone.utc): raise HTTPException(409, "Event is not open for registration")
    existing = db.scalar(select(Registration).where(Registration.event_id == event_id, Registration.user_id == user.id))
    if existing and existing.status == RegistrationStatus.ACTIVE: raise HTTPException(409, "Already registered")
    count = db.scalar(select(func.count()).select_from(Registration).where(Registration.event_id == event_id, Registration.status == RegistrationStatus.ACTIVE)) or 0
    if count >= event.capacity: raise HTTPException(409, "Event is full")
    if existing: existing.status = RegistrationStatus.ACTIVE; existing.cancelled_at = None; reg = existing
    else: reg = Registration(event_id=event_id, user_id=user.id); db.add(reg)
    db.commit(); db.refresh(reg); return reg
def cancel(db: Session, event_id, user: User):
    reg = db.scalar(select(Registration).where(Registration.event_id == event_id, Registration.user_id == user.id, Registration.status == RegistrationStatus.ACTIVE))
    if not reg: raise HTTPException(404, "Active registration not found")
    reg.status = RegistrationStatus.CANCELLED; reg.cancelled_at = datetime.now(timezone.utc); db.commit(); db.refresh(reg); return reg
def mine(db, user_id): return list(db.scalars(select(Registration).where(Registration.user_id == user_id).order_by(Registration.registered_at.desc())))
def for_event(db, event_id): return list(db.scalars(select(Registration).where(Registration.event_id == event_id).order_by(Registration.registered_at)))
