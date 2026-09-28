from collections import Counter
from app.schemas.log_event import LogEvent


def group_messages(events: list[LogEvent]) -> list[dict]:
    message_counts = Counter(
        event.message.strip() for event in events if event.message.strip()
    )
    groups = []
    for message, count in message_counts.most_common():
        groups.append({"message": message, "count": count})
    return groups
