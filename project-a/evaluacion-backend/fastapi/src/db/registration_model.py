import uuid
from sqlalchemy import Column, String, ForeignKey, UUID
from src.db.base import Base

class RegistrationModel(Base):
    __tablename__ = "registration"
    __table_args__ = {"schema": "content"}
    
    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID, ForeignKey("content.session.id", ondelete="CASCADE"), nullable=False)
    user_email = Column(String(254), nullable=False)
    status = Column(String(20), nullable=False, default="confirmed")