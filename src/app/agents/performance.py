import json
from app.agents.llm import llm
from app.agents.state import AgentState

PERFORMANCE_PROMPT = """
You are the Performance Investigator in an enterprise log analysis system.
Analyze candidate events for:
- high latency
- slow requests
- slow database operations
- timeouts
- excessive retries
- throughput degradation
- queue delays

Do not invent evidence.
Return JSON:

{
  "findings": [
    {
      "category": "...",
      "title": "...",
      "severity": "LOW|MEDIUM|HIGH|CRITICAL",
      "description": "...",
      "evidence": "...",
      "potential_root_cause": "...",
      "potential_impact": "...",
      "confidence": 0.0
    }
  ]
}
If no meaningful performance issue exists:

{"findings": []}
"""


def performance_agent(state: AgentState) -> AgentState:
    candidates = state.get("candidates", [])
    evidence = state.get("evidence", [])
    performance_candidates = [
        candidate
        for candidate in candidates
        if candidate.get("type") in {"error_spike", "performance_issue"}
    ]
    if not performance_candidates:
        return {"performance_findings": []}
    relevant_evidence = [
        item for item in evidence if item.get("candidate") in performance_candidates
    ]
    prompt = f"""
{PERFORMANCE_PROMPT}

Candidate events:

{json.dumps(performance_candidates, indent=2)}

Supporting log evidence:

{json.dumps(relevant_evidence, indent=2)}
"""
    response = llm.invoke(prompt)
    try:
        result = json.loads(response.content)
    except json.JSONDecodeError:
        result = {"findings": []}
    return {"performance_findings": result.get("findings", [])}
