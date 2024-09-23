# model/retriever.py

from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from model.config import FAISS_INDEX_PATH, OPENAI_API_KEY

def get_retriever():
    embeddings = OpenAIEmbeddings(model="text-embedding-ada-002", openai_api_key=OPENAI_API_KEY)
    vector_store = FAISS.load_local(FAISS_INDEX_PATH, embeddings, allow_dangerous_deserialization=True)

    retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 3})
    return retriever
