from __future__ import annotations

DEFAULT_RELEVANCE_THRESHOLD = 0.50


def filter_by_relevance(
    results: list[dict], threshold: float = DEFAULT_RELEVANCE_THRESHOLD
) -> list[dict]:
    """
    Remove chunks below the minimum relevance threshold.
    """
    filtered = [
        result for result in results if result.get("relevance_score", 0.0) >= threshold
    ]
    return filtered
