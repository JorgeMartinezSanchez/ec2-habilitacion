import uuid
from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.db.base import Base
from src.db.session_speaker import session_speaker_table

if TYPE_CHECKING:
    from src.db.session_model import SessionModel

class SpeakerModel(Base):
    __tablename__ = "speaker"
    __table_args__ = {"schema": "content"}

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column()
    affiliation: Mapped[str | None] = mapped_column()
    bio: Mapped[str | None] = mapped_column()

    sessions: Mapped[list["SessionModel"]] = relationship(
        secondary=session_speaker_table,
        viewonly=True,
    )