from datetime import datetime, timezone
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field, model_validator
from app.models.event import EventStatus
class EventCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200); description: str | None = None; venue_id: UUID; starts_at: datetime; ends_at: datetime; capacity: int = Field(gt=0); status: EventStatus = EventStatus.DRAFT
    @model_validator(mode="after")
    def valid_times(self):
        if self.starts_at >= self.ends_at: raise ValueError("starts_at must be before ends_at")
        return self
class EventUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200); description: str | None = None; venue_id: UUID | None = None; starts_at: datetime | None = None; ends_at: datetime | None = None; capacity: int | None = Field(default=None, gt=0); status: EventStatus | None = None
class EventOut(EventCreate):
    model_config = ConfigDict(from_attributes=True)
    id: UUID; created_by: UUID
