from src.client.database import DBClient
from src.db.message import Message
from src.db.user import User
from src.schema.message import MessageRequest, MessageResponse


class MessageService:

    @classmethod
    def get_all_messages(cls, user: User, db_client: DBClient) -> list[MessageResponse]:
        messages = db_client.query(
            Message.get_by_field_multiple,
            field="user_id",
            match_value=user.id,
            error_not_exist=False,
        )
        if messages is None:
            return []
        return [
            MessageResponse(
                message=message.message,
                role=message.role,
                message_id=message.id,
                created_at=message.created_at,
            )
            for message in messages
        ]

    @classmethod
    def get_ai_reply(
        cls, request: MessageRequest, user: User, db_client: DBClient
    ) -> MessageResponse:
        question = Message(
            message=request.question, user_id=user.id, role="User", status="Pending"
        )
        question.status = "Done"
        answer = Message(
            message="I am a bot", user_id=user.id, role="AI", status="Done"
        )
        db_client.query(Message.add, items=[question, answer])
        return MessageResponse(
            message=answer.message,
            role=answer.role,
            message_id=answer.id,
            created_at=answer.created_at,
        )
