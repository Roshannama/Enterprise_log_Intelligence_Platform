from app.agents.state import AgentState
from app.services.evidence_retriever import (
    find_events_by_id,
    find_events_by_message,
    get_context,
)


def evidence_retriever(state: AgentState) -> AgentState:
    events = state.get("events", [])
    candidates = state.get("candidates", [])
    evidence = []
    for candidate in candidates:
        candidate_type = candidate.get("type")
        event_id = candidate.get("event_id")
        if event_id:
            matching_events = find_events_by_id(events, event_id)
            for event in matching_events:
                context = get_context(events, event, window=2)
                evidence.append(
                    {
                        "candidate": candidate,
                        "events": [event.model_dump(mode="json") for event in context],
                    }
                )
            continue
        message = candidate.get("message")
        if message:
            matching_events = find_events_by_message(events, message, limit=5)
            evidence.append(
                {
                    "candidate": candidate,
                    "events": [
                        event.model_dump(mode="json") for event in matching_events
                    ],
                }
            )
    return {"evidence": evidence}
