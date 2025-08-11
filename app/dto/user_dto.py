from pydantic import BaseModel as PydanticBaseModel, EmailStr


class UserCreateDTO(PydanticBaseModel):
    username: str
    email: EmailStr


class UserReadDTO(UserCreateDTO):
    id: int
