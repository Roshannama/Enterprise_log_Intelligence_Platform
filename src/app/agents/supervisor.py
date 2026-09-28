from app.agents.state import AgentState


def supervisor(state: AgentState) -> AgentState:
    candidates = state.get("candidates", [])
    agent_types = set()
    for candidate in candidates:
        candidate_type = candidate.get("type")
        if candidate_type == "potential_security_issue":
            agent_types.add("security")
        elif candidate_type in {"repeated_error", "error_spike"}:
            agent_types.add("reliability")
        elif candidate_type == "performance_issue":
            agent_types.add("performance")
    return {"selected_agent": ",".join(sorted(agent_types))}
