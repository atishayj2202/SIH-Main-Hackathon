from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

class AnswerResponse(BaseModel):
    question_id: UUID
    answer_id: UUID
    status: str
    correct_answer_code: str

class QuestionResponse(BaseModel):
    question_id: UUID
    question: str
    option_a: str
    option_b: str
    option_d: str
    option_c: str


class ActiveGameResponse(BaseModel):
    current_position: str
    status: str
    current_question_progress: float
    current_question: str


class ArchiveGameResponse(BaseModel):
    created_at: datetime
    status: str
    completed_at: datetime | None = None