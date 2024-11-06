from typing import List

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from database import Base, Engine, SessionLocal
from repositories import repository_users
from repositories import repository_rooms
from repositories import repository_bookings
from schemas import schema_user
from schemas import schema_room
from schemas import schema_booking


# 起動設定
Base.metadata.create_all(bind=Engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ルーティング
# get
@app.get("/")
async def index():
    return {"message": "Success"}


@app.get("/users", response_model=List[schema_user.User])
async def read_users(db: Session = Depends(get_db)):
    users = repository_users.get_users(db)
    return users


@app.get("/rooms", response_model=List[schema_room.Room])
async def read_rooms(db: Session = Depends(get_db)):
    rooms = repository_rooms.get_rooms(db)
    return rooms


@app.get("/bookings", response_model=List[schema_booking.Booking])
async def read_bookings(db: Session = Depends(get_db)):
    bookings = repository_bookings.get_bookings(db)
    return bookings


# post
@app.post("/users", response_model=schema_user.User)
async def create_user(user: schema_user.UserCreate, db: Session = Depends(get_db)):
    return repository_users.create_user(db, user)


@app.post("/rooms", response_model=schema_room.Room)
async def create_room(room: schema_room.RoomCreate, db: Session = Depends(get_db)):
    return repository_rooms.create_room(db, room)


@app.post("/bookings", response_model=schema_booking.Booking)
async def create_booking(
    booking: schema_booking.BookingCreate, db: Session = Depends(get_db)
):
    return repository_bookings.create_booking(db, booking)
