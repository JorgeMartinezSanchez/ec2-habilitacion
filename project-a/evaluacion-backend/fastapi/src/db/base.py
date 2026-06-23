from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import MetaData

metadata = MetaData(schema="content")

class Base(DeclarativeBase):
    metadata = metadata
