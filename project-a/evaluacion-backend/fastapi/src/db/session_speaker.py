from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from src.db.base import Base

# Tabla de asociación session_speaker
session_speaker_table = Table(
    "session_speaker",
    Base.metadata,
    Column("session_id", UUID, ForeignKey("content.session.id", ondelete="CASCADE"), primary_key=True),
    Column("speaker_id", UUID, ForeignKey("content.speaker.id", ondelete="CASCADE"), primary_key=True),
    schema="content",
    extend_existing=True
)