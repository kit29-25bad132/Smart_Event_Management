from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID; email: str; role: str; is_active: bool; created_at: datetime

class TokenResponse(BaseModel):
    access_token: str; token_type: str = "bearer"; user: UserOut

class Page(BaseModel):
    page: int; page_size: int; total: int
