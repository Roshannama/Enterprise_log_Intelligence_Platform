from app.schemas.log_event import LogEvent


def find_events_by_message(
    events: list[LogEvent], message: str, limit: int = 10
) -> list[LogEvent]:
    message = message.lower().strip()
    matches = []
    for event in events:
        if message in event.message.lower():
            matches.append(event)
        if len(matches) >= limit:
            break
    return matches


def find_events_by_id(events: list[LogEvent], event_id: str) -> list[LogEvent]:
    return [event for event in events if event.event_id == event_id]


def get_context(
    events: list[LogEvent], event: LogEvent, window: int = 2
) -> list[LogEvent]:
    try:
        index = events.index(event)
    except ValueError:
        return [event]
    start = max(0, index - window)
    end = min(len(events), index + window + 1)
    return events[start:end]
