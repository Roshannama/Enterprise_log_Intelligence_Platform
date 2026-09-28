from app.agents.state import AgentState


def report_generator(state: AgentState) -> AgentState:
    findings = state.get("validated_findings", [])
    rca = state.get("rca", {})
    report = {
        "summary": {
            "total_findings": len(findings),
            "incident": rca.get("incident", "No major incident identified"),
        },
        "findings": findings,
        "root_cause_analysis": rca,
    }
    return {"final_report": report}
