from app.schemas.log_event import LogEvent
from app.services.analytics.anomaly import detect_error_spikes
from app.services.analytics.grouping import group_messages
from app.services.analytics.statistics import calculate_statistics


def analyze_events(events: list[LogEvent]) -> dict:
    statistics = calculate_statistics(events)
    message_groups = group_messages(events)
    anomalies = detect_error_spikes(events)
    candidates = []
    for group in message_groups:
        if group["count"] >= 3:
            candidates.append(
                {
                    "type": "repeated_error",
                    "category": "reliability",
                    "message": group["message"],
                    "count": group["count"],
                }
            )
    for anomaly in anomalies:
        candidates.append({**anomaly, "category": "reliability"})
    for event in events:
        sanitized_items = event.metadata.get("sanitized_items", [])
        if sanitized_items:
            candidates.append(
                {
                    "type": "potential_security_issue",
                    "category": "security",
                    "event_id": event.event_id,
                    "message": event.message,
                    "count": 1,
                    "detected_sensitive_data": sanitized_items,
                }
            )
    return {
        "statistics": statistics,
        "message_groups": message_groups[:20],
        "anomalies": anomalies,
        "candidates": candidates,
    }
