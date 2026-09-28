from datetime import datetime
from typing import Any
from pydantic import BaseModel, Field


class LogEvent(BaseModel):
    event_id: str
    timestamp: datetime | None = None
    severity: str | None = None
    service: str | None = None
    component: str | None = None
    request_id: str | None = None
    trace_id: str | None = None
    message: str
    source_file: str
    line_start: int | None = None
    line_end: int | None = None
    raw_log: str
    metadata: dict[str, Any] = Field(default_factory=dict)
