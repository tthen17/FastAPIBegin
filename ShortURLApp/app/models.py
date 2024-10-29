from sqlalchemy import Column, String

from .database import Base


class Url(Base):
    __tablename__ = "urlbase"

    short_url = Column(String, primary_key=True, index=True)
    original_url = Column(String, index=True)