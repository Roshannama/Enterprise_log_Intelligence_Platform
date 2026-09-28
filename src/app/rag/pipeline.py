from __future__ import annotations
from app.rag.context import build_rag_context
from app.rag.citations import build_citations
from app.rag.filter import filter_by_relevance
from app.rag.hybrid_retriever import hybrid_search
from app.rag.reorder import reorder_context
from app.rag.reranker import rerank_results


def retrieve_knowledge(
    query: str,
    dense_k: int = 10,
    sparse_k: int = 10,
    rerank_k: int = 8,
    final_k: int = 5,
    relevance_threshold: float = 0.50,
) -> dict:
    """
    Complete RAG retrieval pipeline.

    Pipeline:

    Dense + Sparse
        ↓
    Hybrid candidates
        ↓
    Reranker
        ↓
    Relevance threshold
        ↓
    Context reordering
        ↓
    Final context + citations
    """
    hybrid_results = hybrid_search(query=query, dense_k=dense_k, sparse_k=sparse_k)
    reranked_results = rerank_results(
        query=query, results=hybrid_results, top_k=rerank_k
    )
    filtered_results = filter_by_relevance(
        results=reranked_results, threshold=relevance_threshold
    )
    filtered_results = filtered_results[:final_k]
    reordered_results = reorder_context(filtered_results)
    context = build_rag_context(reordered_results)
    citations = build_citations(reordered_results)
    return {
        "query": query,
        "results": reordered_results,
        "context": context,
        "citations": citations,
    }
