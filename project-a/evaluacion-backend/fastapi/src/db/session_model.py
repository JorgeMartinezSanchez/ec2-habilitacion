import uuid
from datetime import datetime
from sqlalchemy import Table, Column, String, ForeignKey, UUID, DateTime, Integer, MetaData
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import relationship
from src.db.base import Base

# Tabla de asociación para session_speaker
session_speaker_table = Table(
    "session_speaker",
    Base.metadata,
    Column("session_id", UUID, ForeignKey("content.session.id", ondelete="CASCADE"), primary_key=True),
    Column("speaker_id", UUID, ForeignKey("content.speaker.id", ondelete="CASCADE"), primary_key=True),
    schema="content",
    extend_existing=True
)

class SessionModel(Base):
    __table__ = Table(
        "session",
        Base.metadata,
        Column("id", UUID, primary_key=True, default=uuid.uuid4),
        Column("track_id", UUID, ForeignKey("content.track.id", ondelete="CASCADE"), nullable=False),
        Column("title", String(300), nullable=False),
        Column("abstract", String, nullable=True),
        Column("starts_at", TIMESTAMP(timezone=True), nullable=False),
        Column("ends_at", TIMESTAMP(timezone=True), nullable=False),
        Column("capacity", Integer, nullable=True),
        schema="content",
        extend_existing=True
    )
    
    track = relationship("TrackModel", back_populates="sessions", lazy="noload")
    speakers = relationship("SpeakerModel", secondary=session_speaker_table, viewonly=True)