from app.agents.state import AgentState
from app.services.severity.engine import assign_severity


def severity_agent(state: AgentState) -> AgentState:
    findings = state.get("validated_findings", [])
    findings_with_severity = assign_severity(findings)
    return {"validated_findings": findings_with_severity}
