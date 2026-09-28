from __future__ import annotations
from pathlib import Path
from app.agents.graph import build_graph
from app.services.analytics.engine import analyze_events
from app.services.parsers import parse_file
from app.services.sanitizer import sanitize_events


async def analyze_log_file(file_path: str, source_file: str | None = None) -> dict:
    path = Path(file_path)
    events = parse_file(str(path), source_file or path.name)
    events = sanitize_events(events)
    analysis = analyze_events(events)
    graph = build_graph()
    initial_state = {
        "events": events,
        "candidates": analysis["candidates"],
        "file_id": path.stem,
        "filename": path.name,
    }
    result = await graph.ainvoke(initial_state)
    return {"analysis": analysis, "report": result.get("final_report", {})}
