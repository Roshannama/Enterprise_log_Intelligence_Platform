from __future__ import annotations
import pickle
import re
from pathlib import Path
from rank_bm25 import BM25Okapi
from app.rag.chunker import chunk_documents
from app.rag.loader import load_documents
from app.rag.vector_store import get_vector_store

BM25_DIR = Path("storage/bm25")
BM25_FILE = BM25_DIR / "bm25_index.pkl"


def tokenize(text: str) -> list[str]:
    """
    Tokenize text for BM25 retrieval.

    Keeps technical tokens such as:
    database
    PaymentService
    connection_pool
    HTTP500
    timeout
    """
    return re.findall(r"[A-Za-z0-9_./:-]+", text.lower())


def build_bm25_index() -> None:
    """
    Build BM25 index using the same semantic chunks
    that are stored in Pinecone.
    """
    documents = load_documents("knowledge")
    chunks = chunk_documents(documents)
    texts = [chunk["text"] for chunk in chunks]
    tokenized_texts = [tokenize(text) for text in texts]
    bm25 = BM25Okapi(tokenized_texts)
    BM25_DIR.mkdir(parents=True, exist_ok=True)
    with open(BM25_FILE, "wb") as file:
        pickle.dump({"bm25": bm25, "chunks": chunks}, file)
    print(f"BM25 index created with {len(chunks)} chunks.")


def load_bm25_index() -> tuple[BM25Okapi, list[dict]]:
    """
    Load the persisted BM25 index.
    """
    if not BM25_FILE.exists():
        raise FileNotFoundError(
            "BM25 index not found. " "Run build_bm25_index() first."
        )
    with open(BM25_FILE, "rb") as file:
        data = pickle.load(file)
    return data["bm25"], data["chunks"]


def dense_search(query: str, top_k: int = 10) -> list[dict]:
    """
    Semantic retrieval using Pinecone.
    """
    vector_store = get_vector_store()
    results = vector_store.similarity_search_with_score(query, k=top_k)
    dense_results = []
    for rank, (document, score) in enumerate(results, start=1):
        dense_results.append(
            {
                "text": document.page_content,
                "metadata": document.metadata,
                "retrieval_type": "dense",
                "dense_rank": rank,
                "dense_score": float(score),
            }
        )
    return dense_results


def sparse_search(query: str, top_k: int = 10) -> list[dict]:
    """
    Keyword-based retrieval using BM25.
    """
    bm25, chunks = load_bm25_index()
    query_tokens = tokenize(query)
    scores = bm25.get_scores(query_tokens)
    ranked_indices = sorted(
        range(len(scores)), key=lambda index: scores[index], reverse=True
    )
    sparse_results = []
    for rank, index in enumerate(ranked_indices[:top_k], start=1):
        chunk = chunks[index]
        sparse_results.append(
            {
                "text": chunk["text"],
                "metadata": {
                    "source": chunk["source"],
                    "chunk_id": chunk["chunk_id"],
                    "document_title": chunk["document_title"],
                },
                "retrieval_type": "sparse",
                "sparse_rank": rank,
                "sparse_score": float(scores[index]),
            }
        )
    return sparse_results


def get_chunk_key(result: dict) -> str:
    """
    Generate a stable identifier for a retrieved chunk.
    """
    metadata = result.get("metadata", {})
    chunk_id = metadata.get("chunk_id")
    if chunk_id:
        return chunk_id
    return metadata.get("source", "") + "::" + result.get("text", "")


def deduplicate_results(results: list[dict]) -> list[dict]:
    """
    Remove duplicate chunks while preserving
    the strongest available retrieval information.
    """
    unique_results = {}
    for result in results:
        key = get_chunk_key(result)
        if key not in unique_results:
            unique_results[key] = result
        else:
            existing = unique_results[key]
            existing["retrieval_type"] = "hybrid"
            if "dense_score" in result:
                existing["dense_score"] = result["dense_score"]
                existing["dense_rank"] = result["dense_rank"]
            if "sparse_score" in result:
                existing["sparse_score"] = result["sparse_score"]
                existing["sparse_rank"] = result["sparse_rank"]
    return list(unique_results.values())


def hybrid_search(query: str, dense_k: int = 10, sparse_k: int = 10) -> list[dict]:
    """
    Perform dense + sparse retrieval.

    No RRF or score fusion is performed here.

    The results are simply combined and deduplicated.
    The reranker will determine final relevance later.
    """
    dense_results = dense_search(query=query, top_k=dense_k)
    sparse_results = sparse_search(query=query, top_k=sparse_k)
    combined_results = dense_results + sparse_results
    hybrid_results = deduplicate_results(combined_results)
    return hybrid_results
