from uuid import UUID

from pydantic import BaseModel


class UserCreateRequest(BaseModel):
    email: str
    name: str
    firebase_user_id: str


class UserResponse(BaseModel):
    id: UUID
    email: str
    name: str
