from app.agents.state import AgentState


def evidence_critic(state: AgentState) -> AgentState:
    findings = state.get("combined_findings", [])
    validated = []
    for finding in findings:
        evidence = finding.get("evidence")
        if not evidence:
            continue
        confidence = finding.get("confidence", 0)
        if confidence < 0.4:
            continue
        validated.append(finding)
    return {"validated_findings": validated}
