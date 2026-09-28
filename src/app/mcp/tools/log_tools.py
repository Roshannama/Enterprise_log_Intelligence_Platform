from __future__ import annotations
from pathlib import Path
from app.mcp.config import UPLOAD_DIR
from app.services.evidence_retriever import find_events_by_message, get_context
from app.services.parsers import parse_file


def load_log_events(filename: str):
    """
    Load and parse a log file from the uploads directory.
    """
    safe_filename = Path(filename).name
    file_path = UPLOAD_DIR / safe_filename
    if not file_path.exists():
        raise FileNotFoundError(f"Log file not found: {safe_filename}")
    return parse_file(file_path=str(file_path), source_file=safe_filename)


def search_logs(filename: str, query: str, limit: int = 10) -> list[dict]:
    """
    Search log events by message content.
    """
    events = load_log_events(filename)
    matches = find_events_by_message(events=events, message=query, limit=limit)
    return [event.model_dump(mode="json") for event in matches]


def get_log_context(filename: str, event_id: str, window: int = 2) -> list[dict]:
    """
    Retrieve surrounding log events for a specific event.
    """
    events = load_log_events(filename)
    matching_events = [event for event in events if event.event_id == event_id]
    if not matching_events:
        return []
    context = get_context(events=events, event=matching_events[0], window=window)
    return [event.model_dump(mode="json") for event in context]
