import enum, uuid
from sqlalchemy import Boolean, Enum, String, Index, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base, TimestampMixin, uuid_column

class UserRole(str, enum.Enum):
    ADMIN = "ADMIN"
    USER = "USER"

class User(TimestampMixin, Base):
    __tablename__ = "users"
    __table_args__ = (Index("uq_users_email_lower", text("lower(email)"), unique=True),)
    id: Mapped[uuid.UUID] = uuid_column()
    email: Mapped[str] = mapped_column(String(320), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole, name="user_role"), default=UserRole.USER, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    events = relationship("Event", back_populates="creator")
    registrations = relationship("Registration", back_populates="user")
