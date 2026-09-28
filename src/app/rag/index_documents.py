from app.rag.loader import load_documents
from app.rag.chunker import chunk_documents
from app.rag.vector_store import create_vector_store


def build_knowledge_index():
    print("Loading documents...")
    documents = load_documents("knowledge")
    print(f"Loaded {len(documents)} documents.")
    print("Creating semantic chunks...")
    chunks = chunk_documents(documents)
    print(f"Created {len(chunks)} chunks.")
    print("Uploading to Pinecone...")
    create_vector_store(chunks)
    print("Knowledge successfully indexed in Pinecone.")


if __name__ == "__main__":
    build_knowledge_index()
