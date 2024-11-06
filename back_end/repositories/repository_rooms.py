from sqlalchemy.orm import Session

from schemas import schema_room
from models import model_room


# 会議室一覧取得
def get_rooms(db: Session):
    return db.query(model_room.Room).all()


# 会議室登録
def create_room(db: Session, room: schema_room.Room):
    db_room = model_room.Room(room_name=room.room_name, capacity=room.capacity)
    db.add(db_room)
    db.commit()
    db.refresh(db_room)

    return db_room
