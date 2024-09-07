from uuid import UUID

from pydantic import BaseModel


class MessageResponse(BaseModel):
    message_id: UUID
    message: str
    role: str
    created_at: str


class MessageRequest(BaseModel):
    question: str
