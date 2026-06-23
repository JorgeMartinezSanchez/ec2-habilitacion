import uuid
from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.db.base import Base
from src.db.session_speaker import session_speaker_table

if TYPE_CHECKING:
    from src.db.speaker_model import SpeakerModel
    from src.db.track_model import TrackModel

class SessionModel(Base):
    __tablename__ = "session"
    __table_args__ = {"schema": "content"}
    
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    track_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("content.track.id", ondelete="CASCADE"))
    title: Mapped[str] = mapped_column()
    abstract: Mapped[str | None] = mapped_column()
    starts_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True))
    ends_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True))
    capacity: Mapped[int | None] = mapped_column()
    
    #track = relationship("TrackModel", lazy="noload")
    #speakers: Mapped[list["SpeakerModel"]] = relationship(
    #    secondary=session_speaker_table,
    #    viewonly=True,
    #)