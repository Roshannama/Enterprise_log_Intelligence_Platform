from collections import Counter
from app.schemas.log_event import LogEvent


def calculate_statistics(events: list[LogEvent]) -> dict:
    severity_counts = Counter(event.severity for event in events if event.severity)
    service_counts = Counter(event.service for event in events if event.service)
    return {
        "total_events": len(events),
        "severity_counts": dict(severity_counts),
        "service_counts": dict(service_counts),
    }
