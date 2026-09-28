import asyncio
import json
from app.agents.graph import build_graph
from app.schemas.log_event import LogEvent


async def main():
    events = [
        LogEvent(
            event_id="evt-001",
            timestamp="2026-09-27T10:00:00",
            severity="ERROR",
            service="payment-service",
            component="database",
            request_id="req-001",
            trace_id="trace-001",
            message=(
                "Database connection timeout " "while executing payment transaction"
            ),
            source_file="sample.log",
            line_start=1,
            line_end=1,
            raw_log=(
                "2026-09-27 10:00:00 ERROR "
                "payment-service "
                "Database connection timeout "
                "while executing payment transaction"
            ),
            metadata={},
        ),
        LogEvent(
            event_id="evt-002",
            timestamp="2026-09-27T10:01:00",
            severity="ERROR",
            service="payment-service",
            component="database",
            request_id="req-002",
            trace_id="trace-002",
            message=(
                "Database connection timeout " "while executing payment transaction"
            ),
            source_file="sample.log",
            line_start=2,
            line_end=2,
            raw_log=(
                "2026-09-27 10:01:00 ERROR "
                "payment-service "
                "Database connection timeout "
                "while executing payment transaction"
            ),
            metadata={},
        ),
        LogEvent(
            event_id="evt-003",
            timestamp="2026-09-27T10:02:00",
            severity="ERROR",
            service="payment-service",
            component="database",
            request_id="req-003",
            trace_id="trace-003",
            message=(
                "Database connection timeout " "while executing payment transaction"
            ),
            source_file="sample.log",
            line_start=3,
            line_end=3,
            raw_log=(
                "2026-09-27 10:02:00 ERROR "
                "payment-service "
                "Database connection timeout "
                "while executing payment transaction"
            ),
            metadata={},
        ),
    ]
    initial_state = {
        "events": events,
        "candidates": [
            {
                "type": "repeated_error",
                "category": "reliability",
                "message": (
                    "Database connection timeout " "while executing payment transaction"
                ),
                "count": 3,
            }
        ],
    }
    graph = build_graph()
    print("\nStarting complete LangGraph...\n")
    result = await graph.ainvoke(initial_state)
    print("\n==============================")
    print("FINAL GRAPH STATE")
    print("==============================\n")
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    asyncio.run(main())
