from datetime import datetime
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


class SubCategoryResponse(BaseModel):
    id: UUID
    name: str
    description: str | None = None


class CategoryInfoResponse(BaseModel):
    id: UUID
    name: str
    description: str | None = None
    created_at: datetime
    parent_id: UUID | None = None
    children: list[SubCategoryResponse] = []
