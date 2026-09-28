from app.schemas.log_event import LogEvent
from app.services.sanitizer import sanitize_text


def sanitize_event(event: LogEvent) -> LogEvent:
    clean_message, detected_items = sanitize_text(event.message)
    clean_raw_log, _ = sanitize_text(event.raw_log)
    metadata = dict(event.metadata)
    if detected_items:
        metadata["sanitized"] = True
        metadata["sanitized_items"] = detected_items
    else:
        metadata["sanitized"] = False
    return event.model_copy(
        update={
            "message": clean_message,
            "raw_log": clean_raw_log,
            "metadata": metadata,
        }
    )


def sanitize_events(events: list[LogEvent]) -> list[LogEvent]:
    return [sanitize_event(event) for event in events]
