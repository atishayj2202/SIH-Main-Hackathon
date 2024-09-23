# model/ingest.py

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

from src.client.model.config import FAISS_INDEX_PATH, MARKDOWN_PATH, OPENAI_API_KEY


def ingest_documents():
    loader = DirectoryLoader(MARKDOWN_PATH, glob="**/*.md")
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = text_splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings(
        model="text-embedding-ada-002", openai_api_key=OPENAI_API_KEY
    )
    vector_store = FAISS.from_documents(docs, embeddings)
    vector_store.save_local(FAISS_INDEX_PATH)


if __name__ == "__main__":
    ingest_documents()
