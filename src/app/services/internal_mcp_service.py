from __future__ import annotations
from pathlib import Path
from typing import Any
from app.mcp.tools.log_tools import get_log_context, search_logs
from app.mcp.tools.service_tools import get_service_metadata

def _build_query(finding: dict[str, Any]) -> str:
    title = str(finding.get("title", "")).strip()
    description = str(finding.get("description", "")).strip()
    message = str(finding.get("message", "")).strip()
    category = str(finding.get("category", "")).strip()
    parts = []
    if title:
        parts.append(title)
    if message:
        parts.append(message)
    if description:
        parts.append(description)
    if category:
        parts.append(category)
    query = " ".join(parts)
    return query[:500]

async def search_internal_logs_for_finding(
    finding: dict[str, Any], file_id: str = "", filename: str = ""
) -> dict[str, Any]:
    if not filename:
        return {"available": False, "reason": ("No uploaded filename available.")}
    extension = Path(filename).suffix.lower()
    if not extension:
        return {
            "available": False,
            "reason": ("Could not determine " "file extension."),
        }
    stored_filename = f"{file_id}{extension}" if file_id else filename
    query = _build_query(finding)
    result: dict[str, Any] = {
        "available": True,
        "source": "internal_log_mcp",
        "filename": filename,
        "stored_filename": stored_filename,
        "query": query,
        "log_matches": [],
        "log_context": [],
        "service_metadata": {},
    }
    if query:
        try:
            matches = search_logs(filename=stored_filename, query=query, limit=10)
            result["log_matches"] = matches
            for event in matches[:3]:
                event_id = event.get("event_id")
                if not event_id:
                    continue
                try:
                    context = get_log_context(
                        filename=stored_filename, event_id=event_id, window=2
                    )
                    result["log_context"].append(
                        {"event_id": event_id, "events": context}
                    )
                except Exception:
                    continue
        except Exception as exc:
            result["log_search_error"] = str(exc)
    service = finding.get("service")
    try:
        result["service_metadata"] = get_service_metadata(
            filename=stored_filename, service=service
        )
    except Exception as exc:
        result["service_metadata_error"] = str(exc)
    return result
