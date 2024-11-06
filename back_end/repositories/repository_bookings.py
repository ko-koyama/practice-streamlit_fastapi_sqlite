from sqlalchemy.orm import Session

from schemas import schema_booking
from models import model_booking


# 予約一覧取得
def get_bookings(db: Session):
    return db.query(model_booking.Booking).all()


# 予約登録
def create_booking(db: Session, booking: schema_booking.Booking):
    db_booking = model_booking.Booking(
        user_id=booking.user_id,
        room_id=booking.room_id,
        booked_num=booking.booked_num,
        start_datetime=booking.start_datetime,
        end_datetime=booking.end_datetime,
    )
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)

    return db_booking
