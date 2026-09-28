from __future__ import annotations


def build_rag_context(results: list[dict]) -> str:
    """
    Build a structured context string for the LLM.
    """
    if not results:
        return "No relevant knowledge was retrieved."
    sections = []
    for index, result in enumerate(results, start=1):
        metadata = result.get("metadata", {})
        source = metadata.get("source", "unknown")
        chunk_id = metadata.get("chunk_id", "unknown")
        title = metadata.get("document_title", "unknown")
        relevance = result.get("relevance_score", 0.0)
        section = f"""
[Knowledge {index}]

Source: {source}
Chunk ID: {chunk_id}
Document: {title}
Relevance Score: {relevance:.3f}

Content:
{result["text"]}
""".strip()
        sections.append(section)
    return "\n\n".join(sections)
