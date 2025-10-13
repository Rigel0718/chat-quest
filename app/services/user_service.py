from sqlalchemy.orm import Session

from app.db.schema import User
from app.models.user import UserRead

class UserService:
    def __init__(self, session: Session):
        self._db = session

    def _to_read_model(self, user: User | None) -> UserRead | None:
        if not user:
            return None
        return UserRead.model_validate(user)

    def list_users(self) -> list[UserRead]:
        users = self._db.query(User).all()
        return [UserRead.model_validate(user) for user in users]

    def get_user(self, user_id: int) -> UserRead | None:
        user = self._db.query(User).filter(User.id == user_id).first()
        return self._to_read_model(user)

    def create_user(self, username: str, password: str) -> UserRead:
        user = User(username=username, password=password)
        self._db.add(user)
        self._db.commit()
        self._db.refresh(user)
        return self._to_read_model(user)

    def update_user(self, user_id: int, username: str, password: str) -> UserRead | None:
        user = self._db.query(User).filter(User.id == user_id).first()
        if not user:
            return None
        user.username = username
        user.password = password
        self._db.commit()
        self._db.refresh(user)
        return self._to_read_model(user)

    def delete_user(self, user_id: int) -> bool:
        user = self._db.query(User).filter(User.id == user_id).first()
        if not user:
            return False
        self._db.delete(user)
        self._db.commit()
        return True
