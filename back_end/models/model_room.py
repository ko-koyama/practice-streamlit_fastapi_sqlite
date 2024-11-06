from sqlalchemy import Column, Integer, String
from database import Base


class Room(Base):
    __tablename__ = "rooms"
    room_id = Column(Integer, primary_key=True)
    room_name = Column(String, unique=True, nullable=False)
    capacity = Column(Integer)
