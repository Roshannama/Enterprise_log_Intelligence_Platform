from __future__ import annotations
from collections import Counter
from pathlib import Path
from app.mcp.tools.log_tools import load_log_events
def get_service_metadata(filename: str, service: str | None = None) -> dict:
    """
    Return basic metadata about services
    found in a log file.
    """
    events = load_log_events(filename)
    service_counts = Counter(event.service for event in events if event.service)
    if service:
        matching_events = [event for event in events if event.service == service]
        if not matching_events:
            return {"service": service, "found": False}
        severity_counts = Counter(
            event.severity for event in matching_events if event.severity
        )
        return {
            "service": service,
            "found": True,
            "total_events": len(matching_events),
            "severity_counts": dict(severity_counts),
        }
    return {"services": dict(service_counts), "total_events": len(events)}
