from http.client import responses

from model.ingest import ingest_documents
from model.qa import ask_question
from model.global_model import global_model


class Model:
    def __init__(self):
        pass

    def ingest_documents(self):
        ingest_documents()

    def rag_question(self, question, chat_history) -> dict:
        response = ask_question(question, chat_history)
        return response

    def global_model(self, question, messages) -> str:
        if question:
            messages.append(
                {"role": "user", "content": question},
            )
            model = global_model("gpt-4",messages)
        response = model.choices[0].message.content
        return response