from __future__ import annotations
import math
from sentence_transformers import CrossEncoder

RERANKER_MODEL = "BAAI/bge-reranker-base"

_reranker = None


def get_reranker() -> CrossEncoder:
    """
    Load the reranker lazily.

    The model is loaded only when reranking is actually required.
    """
    global _reranker
    if _reranker is None:
        _reranker = CrossEncoder(RERANKER_MODEL)
    return _reranker


def normalize_score(score: float) -> float:
    """
    Convert the cross-encoder logit into a 0-1
    relevance score using sigmoid.

    This is a relevance score, not a calibrated probability.
    """
    score = max(min(score, 50), -50)
    return 1 / (1 + math.exp(-score))


def rerank_results(query: str, results: list[dict], top_k: int = 8) -> list[dict]:
    """
    Rerank hybrid retrieval candidates.
    """
    if not results:
        return []
    model = get_reranker()
    pairs = [(query, result["text"]) for result in results]
    scores = model.predict(pairs, show_progress_bar=False)
    reranked = []
    for result, raw_score in zip(results, scores):
        raw_score = float(raw_score)
        reranked.append(
            {
                **result,
                "reranker_score": raw_score,
                "relevance_score": normalize_score(raw_score),
            }
        )
    reranked.sort(key=lambda item: item["relevance_score"], reverse=True)
    return reranked[:top_k]
