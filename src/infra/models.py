from sqlalchemy import Column
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, relationship

from config.types import MarkTypes

Base = declarative_base()


class Mark(Base):
    __tablename__ = "marks"

    name = Column(String, primary_key=True)
    type = Column(SQLEnum(MarkTypes), nullable=False)
    current = Column(Float, nullable=False, default=0)
    required = Column(Integer, nullable=False, default=0)

    cards = relationship("Card", back_populates="mark", cascade="all, delete-orphan")


class Card(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    value = Column(Float, nullable=False, default=0)
    mark_name = Column(
        String, ForeignKey("marks.name", ondelete="CASCADE"), nullable=False
    )

    mark = relationship("Mark", back_populates="cards")
