from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import create_db_session
from app.common.exceptions.app_exception import AppException
from app.dto.user_dto import UserCreateDTO, UserReadDTO
from app.repository.user_repository import UserRepository

router = APIRouter()


@router.post("/", response_model=UserReadDTO)
def create(user: UserCreateDTO, db: Session = Depends(create_db_session)):
    user_repository = UserRepository(db)
    db_user = user_repository.get_user_by_username(user.username)
    if db_user:
        raise AppException(code=400, message="Username already registered")
    return user_repository.create(user)
