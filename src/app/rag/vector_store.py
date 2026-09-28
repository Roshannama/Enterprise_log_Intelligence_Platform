from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore
from app.core.config import PINECONE_API_KEY, PINECONE_INDEX_NAME
from app.rag.embeddings import get_embedding_model


def get_pinecone_index():
    """
    Connect to the Pinecone index.
    """
    if not PINECONE_API_KEY:
        raise ValueError("PINECONE_API_KEY is not configured.")
    if not PINECONE_INDEX_NAME:
        raise ValueError("PINECONE_INDEX_NAME is not configured.")
    pc = Pinecone(api_key=PINECONE_API_KEY)
    return pc.Index(PINECONE_INDEX_NAME)


def create_vector_store(chunks: list[dict]):
    """
    Add knowledge chunks to Pinecone.
    """
    embedding_model = get_embedding_model()
    texts = [chunk["text"] for chunk in chunks]
    metadatas = [
        {
            "source": chunk["source"],
            "chunk_id": chunk["chunk_id"],
            "document_title": chunk["document_title"],
        }
        for chunk in chunks
    ]
    vector_store = PineconeVectorStore(
        index=get_pinecone_index(), embedding=embedding_model
    )
    vector_store.add_texts(texts=texts, metadatas=metadatas)
    return vector_store


def get_vector_store():
    """
    Connect to the existing Pinecone vector store.
    """
    embedding_model = get_embedding_model()
    return PineconeVectorStore(index=get_pinecone_index(), embedding=embedding_model)
