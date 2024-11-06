from sqlalchemy.orm import Session

from schemas import schema_user
from models import model_user


# ユーザ一覧取得
def get_users(db: Session):
    return db.query(model_user.User).all()


# ユーザ登録
def create_user(db: Session, user: schema_user.User):
    db_user = model_user.User(user_name=user.user_name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user
