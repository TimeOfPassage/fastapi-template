from typing import Optional

from sqlalchemy.orm import Session

from app.repository.base_repository import BaseRepository
from app.models.user_model import UserModel


class UserRepository(BaseRepository[UserModel]):

    def __init__(self, db: Session):
        super().__init__(db, UserModel)

    def get_user_by_username(self, username: str) -> Optional[UserModel]:
        return (
            self.db.query(self.model)
            .filter(self.model.username == username)
            .first()
        )
