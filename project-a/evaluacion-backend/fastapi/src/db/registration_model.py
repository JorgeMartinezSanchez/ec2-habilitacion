import uuid
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.db.base import Base
from src.db.session_model import SessionModel

class RegistrationModel(Base):
    __tablename__ = "registration"
    __table_args__ = {"schema": "content"}

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    session_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("content.session.id", ondelete="CASCADE"))
    user_email: Mapped[str] = mapped_column()
    status: Mapped[str] = mapped_column()
    
    session: Mapped["SessionModel"] = relationship("SessionModel", back_populates="registrations")