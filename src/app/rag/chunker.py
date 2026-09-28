import re


def split_into_sections(text: str) -> list[str]:
    """
    Split Markdown document into sections using headings.
    """
    sections = re.split(r"(?=^#{1,3}\s+)", text, flags=re.MULTILINE)
    return [section.strip() for section in sections if section.strip()]


def chunk_documents(documents: list[dict]) -> list[dict]:
    """
    Create semantic chunks from Markdown documents.
    """
    chunks = []
    for document in documents:
        source = document["source"]
        text = document["text"]
        sections = split_into_sections(text)
        document_title = sections[0] if sections else "Unknown Document"
        for index, section in enumerate(sections):
            chunks.append(
                {
                    "chunk_id": f"{source}-{index + 1}",
                    "source": source,
                    "document_title": document_title,
                    "text": section,
                }
            )
    return chunks
