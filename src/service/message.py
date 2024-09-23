from src.client.database import DBClient
from src.client.model import Model
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
        cls, request: MessageRequest, user: User, db_client: DBClient, rag: bool =True
    ) -> MessageResponse:
        question = Message(
            message=request.question, user_id=user.id, role="User", status="Pending"
        )
        question.status = "Done"
        temp = db_client.query(
            Message.get_by_field_multiple,
            field="user_id",
            match_value=user.id,
            error_not_exist=False,
        )
        messages = []
        if temp is not None:
            for message in temp:
                messages.append(
                    {
                        "role": "assistant" if message.role == "AI" else "user",
                        "content": [{"type": "text", "text": message.message}],
                    }
                )
        model_rag = Model()
        if rag:
            temp = model_rag.rag_question(request.question, messages)
            sources = temp["sources"]
            ans = temp["answer"]
        else:
            ans = model_rag.global_model(
                request.question,
                messages,
            )
            sources = None
        answer = Message(
            message=ans,
            user_id=user.id,
            role="AI",
            status="Done",
        )
        db_client.query(Message.add, items=[question, answer])
        return MessageResponse(
            message=answer.message,
            role=answer.role,
            message_id=answer.id,
            created_at=answer.created_at,
            sources=sources,
        )
