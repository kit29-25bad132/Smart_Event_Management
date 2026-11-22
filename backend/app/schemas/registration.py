from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict
from app.models.registration import RegistrationStatus
class RegistrationOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID; event_id: UUID; user_id: UUID; status: RegistrationStatus; registered_at: datetime; cancelled_at: datetime | None
