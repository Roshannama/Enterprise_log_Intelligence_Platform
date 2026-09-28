from collections import Counter
from datetime import datetime
from app.schemas.log_event import LogEvent


def detect_error_spikes(events: list[LogEvent], threshold: int = 10) -> list[dict]:
    hourly_errors = Counter()
    for event in events:
        if not event.timestamp:
            continue
        if event.severity not in {"ERROR", "CRITICAL", "FATAL"}:
            continue
        hour = event.timestamp.replace(minute=0, second=0, microsecond=0)
        hourly_errors[hour] += 1
    anomalies = []
    for hour, count in hourly_errors.items():
        if count >= threshold:
            anomalies.append(
                {
                    "type": "error_spike",
                    "timestamp": hour.isoformat(),
                    "error_count": count,
                    "threshold": threshold,
                    "message": (
                        f"High error volume detected: " f"{count} errors in this hour."
                    ),
                }
            )
    return anomalies
