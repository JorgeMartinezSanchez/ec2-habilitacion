import uuid
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from src.db.base import Base

class TrackModel(Base):
    __tablename__ = "track"
    __table_args__ = {"schema": "content"}

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    conference_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("content.conference.id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column()
    color: Mapped[str | None] = mapped_column()
    description: Mapped[str | None] = mapped_column()

    # Temporalmente comentamos la relación sessions
    # sessions: Mapped[list["SessionModel"]] = relationship(
    #     secondary="content.session_speaker",
    #     viewonly=True,
    # )