import uuid
from datetime import datetime
from sqlalchemy import Table, Column, String, ForeignKey, UUID, DateTime, Integer, MetaData
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship
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
    __table_args__ = {"schema": "content"}
    
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    track_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("content.track.id"))
    title: Mapped[str] = mapped_column()
    abstract: Mapped[str | None] = mapped_column()
    starts_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True))
    ends_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True))
    capacity: Mapped[int | None] = mapped_column()
    
    track = relationship("TrackModel", lazy="noload")
    speakers: Mapped[list["SpeakerModel"]] = relationship(
        secondary=session_speaker_table,
        viewonly=True,
    )