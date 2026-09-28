from __future__ import annotations


def build_citations(results: list[dict]) -> list[dict]:
    """
    Create citation metadata for retrieved knowledge.
    """
    citations = []
    for index, result in enumerate(results, start=1):
        metadata = result.get("metadata", {})
        citations.append(
            {
                "citation_id": f"KNOW-{index:03d}",
                "source": metadata.get("source", "unknown"),
                "chunk_id": metadata.get("chunk_id", "unknown"),
                "document_title": metadata.get("document_title", "unknown"),
                "relevance_score": result.get("relevance_score", 0.0),
            }
        )
    return citations
