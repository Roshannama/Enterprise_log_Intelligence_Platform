import pandas as pd
from app.schemas.log_event import LogEvent


def parse_excel_file(file_path: str, source_file: str) -> list[LogEvent]:
    df = pd.read_excel(file_path)
    events = []
    for index, row in df.iterrows():
        row_data = row.to_dict()
        timestamp = row_data.get("timestamp")
        severity = row_data.get("severity", row_data.get("level"))
        service = row_data.get("service")
        message = row_data.get("message")
        event = LogEvent(
            event_id=f"EVT-{index + 1:06d}",
            timestamp=(
                pd.to_datetime(timestamp, errors="coerce")
                if timestamp is not None
                else None
            ),
            severity=str(severity) if pd.notna(severity) else None,
            service=str(service) if pd.notna(service) else None,
            message=str(message) if pd.notna(message) else str(row_data),
            source_file=source_file,
            line_start=index + 2,
            line_end=index + 2,
            raw_log=str(row_data),
            metadata={"original_columns": list(df.columns)},
        )
        events.append(event)
    return events
