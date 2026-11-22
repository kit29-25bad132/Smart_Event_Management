from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field
class VenueCreate(BaseModel): name: str = Field(min_length=1, max_length=200); capacity: int = Field(gt=0); location: str = Field(min_length=1, max_length=500)
class VenueUpdate(BaseModel): name: str | None = Field(default=None, min_length=1, max_length=200); capacity: int | None = Field(default=None, gt=0); location: str | None = Field(default=None, min_length=1, max_length=500)
class VenueOut(VenueCreate):
    model_config = ConfigDict(from_attributes=True)
    id: UUID; is_active: bool
