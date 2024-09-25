from src.client.model.config import SYSTEM_PROMPT_2
from src.client.model.global_model import global_model
from src.client.model.ingest import ingest_documents
from src.client.model.qa import ask_question


class Model:
    def __init__(self):
        pass

    def ingest_documents(self) -> None:
        ingest_documents()

    def rag_question(self, question, chat_history) -> dict:
        response = ask_question(question, chat_history)
        return response

    def global_model(self, question: str, messages: list) -> str:
        if question:
            messages.append(
                {"role": "user", "content": question},
            )
            model = global_model(messages)
        else:
            return "Unexpected error"
        response = model.choices[0].message.content
        return response
