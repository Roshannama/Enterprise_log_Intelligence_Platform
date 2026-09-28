from langchain_huggingface import HuggingFaceEmbeddings


def get_embedding_model():
    """
    Create the embedding model used by the RAG pipeline.
    """
    return HuggingFaceEmbeddings(model_name="BAAI/bge-base-en-v1.5")


def embed_chunks(chunks: list[dict]) -> list[dict]:
    """
    Generate embeddings for semantic chunks.
    """
    embedding_model = get_embedding_model()
    texts = [chunk["text"] for chunk in chunks]
    embeddings = embedding_model.embed_documents(texts)
    embedded_chunks = []
    for chunk, embedding in zip(chunks, embeddings):
        embedded_chunks.append({**chunk, "embedding": embedding})
    return embedded_chunks
