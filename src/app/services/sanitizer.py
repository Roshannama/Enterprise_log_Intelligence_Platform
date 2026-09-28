import re
from app.schemas.log_event import LogEvent

PATTERNS = [
    (
        "bearer_token",
        re.compile(r"(?i)(Bearer\s+)[A-Za-z0-9\-._~+/]+=*"),
        r"\1[REDACTED]",
    ),
    ("password", re.compile(r"(?i)(password\s*[=:]\s*)[^\s,;]+"), r"\1[REDACTED]"),
    ("api_key", re.compile(r"(?i)(api[_-]?key\s*[=:]\s*)[^\s,;]+"), r"\1[REDACTED]"),
    (
        "email",
        re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"),
        "[REDACTED_EMAIL]",
    ),
]


def sanitize_text(text: str) -> tuple[str, list[str]]:
    sanitized_text = text
    detected_items = []
    for name, pattern, replacement in PATTERNS:
        if pattern.search(sanitized_text):
            detected_items.append(name)
            sanitized_text = pattern.sub(replacement, sanitized_text)
    return sanitized_text, detected_items


def sanitize_events(events: list[LogEvent]) -> list[LogEvent]:
    """
    Sanitize all log events.

    - Removes sensitive information from the log message.
    - Stores what type of sensitive information was detected.
    - Preserves the original event structure.
    """
    sanitized_events = []
    for event in events:
        sanitized_message, detected_items = sanitize_text(event.message)
        metadata = dict(event.metadata or {})
        metadata["sanitized_items"] = detected_items
        sanitized_event = event.model_copy(
            update={"message": sanitized_message, "metadata": metadata}
        )
        sanitized_events.append(sanitized_event)
    return sanitized_events
