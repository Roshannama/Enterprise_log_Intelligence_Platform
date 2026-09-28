from pathlib import Path


def load_documents(knowledge_dir: str) -> list[dict]:
    documents = []
    knowledge_path = Path(knowledge_dir)
    for file_path in knowledge_path.rglob("*.md"):
        text = file_path.read_text(encoding="utf-8")
        documents.append({"source": str(file_path), "text": text})
    return documents
