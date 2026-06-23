import uuid
from datetime import datetime
from sqlalchemy import Column, String, ForeignKey, UUID, DateTime, Integer, Table
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import relationship
from src.db.base import Base

session_speaker_table = Table(
    "session_speaker",
    Base.metadata,
    Column("session_id", UUID, ForeignKey("content.session.id", ondelete="CASCADE"), primary_key=True),
    Column("speaker_id", UUID, ForeignKey("content.speaker.id", ondelete="CASCADE"), primary_key=True),
    schema="content",
    extend_existing=True
)

class SessionModel(Base):
    __tablename__ = "session"
    __table_args__ = {"schema": "content", "extend_existing": True}
    
    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    track_id = Column(UUID, ForeignKey("content.track.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(300), nullable=False)
    abstract = Column(String, nullable=True)
    starts_at = Column(TIMESTAMP(timezone=True), nullable=False)
    ends_at = Column(TIMESTAMP(timezone=True), nullable=False)
    capacity = Column(Integer, nullable=True)
    
    track = relationship("TrackModel", back_populates="sessions", lazy="noload")
    speakers = relationship("SpeakerModel", secondary=session_speaker_table, viewonly=True)