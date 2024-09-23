# model/qa.py
from langchain.chains import RetrievalQA
from langchain.chains.question_answering.map_reduce_prompt import messages
from langchain_openai import ChatOpenAI

from src.client.model.config import OPENAI_API_KEY, SYSTEM_PROMPT
from src.client.model.retriever import get_retriever


def ask_question(query, chat_history):
    llm = ChatOpenAI(
        model="gpt-4",
        temperature=1,
        top_p=1,
        openai_api_key=OPENAI_API_KEY,
    )

    retriever = get_retriever()

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm, chain_type="stuff", retriever=retriever, return_source_documents=True
    )

    messages = (
        "\n".join([f"{msg['role']}: {msg['content']}" for msg in chat_history])
        if chat_history
        else ""
    )
    full_query = f"{SYSTEM_PROMPT}\n{messages}\nuser: {query}"

    result = qa_chain.invoke({"query": full_query})
    response = {
        "answer": result["result"],
        "sources": [doc.metadata["source"] for doc in result["source_documents"]],
    }
    return response
