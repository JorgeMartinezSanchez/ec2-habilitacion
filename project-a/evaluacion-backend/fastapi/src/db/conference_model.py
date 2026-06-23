from datetime import datetime
import uuid
from sqlalchemy import Table, Column, String, DateTime, UUID
from sqlalchemy.orm import declarative_base
from src.db.base import Base

class ConferenceModel(Base):
    __tablename__ = "conference"
    __table_args__ = {"schema": "content", "extend_existing": True}
    
    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    name = Column(String(200), nullable=False)
    slug = Column(String(100), nullable=False, unique=True)
    starts_at = Column(DateTime(timezone=True), nullable=False)
    ends_at = Column(DateTime(timezone=True), nullable=False)
    timezone = Column(String(50), nullable=False, default="UTC")