import re
from datetime import datetime
from app.schemas.log_event import LogEvent

LOG_PATTERN = re.compile(
    r"^(?P<timestamp>\d{4}-\d{2}-\d{2}"
    r"[ T]\d{2}:\d{2}:\d{2})"
    r"\s+"
    r"(?P<severity>DEBUG|INFO|WARNING|WARN|ERROR|CRITICAL|FATAL)"
    r"\s+"
    r"(?P<service>\S+)"
    r"\s+"
    r"(?P<message>.*)$",
    re.IGNORECASE,
)


def parse_log_file(file_path: str, source_file: str) -> list[LogEvent]:
    events = []
    with open(file_path, "r", encoding="utf-8", errors="replace") as file:
        for line_number, line in enumerate(file, start=1):
            raw_line = line.rstrip("\n")
            if not raw_line.strip():
                continue
            match = LOG_PATTERN.match(raw_line)
            if match:
                data = match.groupdict()
                timestamp = datetime.fromisoformat(data["timestamp"].replace(" ", "T"))
                event = LogEvent(
                    event_id=f"EVT-{len(events) + 1:06d}",
                    timestamp=timestamp,
                    severity=data["severity"].upper(),
                    service=data["service"],
                    message=data["message"],
                    source_file=source_file,
                    line_start=line_number,
                    line_end=line_number,
                    raw_log=raw_line,
                )
            else:
                event = LogEvent(
                    event_id=f"EVT-{len(events) + 1:06d}",
                    message=raw_line,
                    source_file=source_file,
                    line_start=line_number,
                    line_end=line_number,
                    raw_log=raw_line,
                    metadata={"parse_status": "unstructured"},
                )
            events.append(event)
    return events
