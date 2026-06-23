import uuid
from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.db.base import Base
from src.db.session_model import session_speaker_table

class SpeakerModel(Base):
    __tablename__ = "speaker"
    __table_args__ = {"schema": "content"}

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    affiliation: Mapped[str | None] = mapped_column()
    bio: Mapped[str | None] = mapped_column()
    
    sessions: Mapped[list["SessionModel"]] = relationship(
        secondary=session_speaker_table,
        viewonly=True,
    )