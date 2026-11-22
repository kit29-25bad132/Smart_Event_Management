import uuid
from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base, TimestampMixin, uuid_column

class Venue(TimestampMixin, Base):
    __tablename__ = "venues"
    id: Mapped[uuid.UUID] = uuid_column()
    name: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    capacity: Mapped[int] = mapped_column(Integer, nullable=False)
    location: Mapped[str] = mapped_column(String(500), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    events = relationship("Event", back_populates="venue")
