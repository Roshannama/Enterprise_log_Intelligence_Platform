import json
from app.agents.llm import llm
from app.agents.state import AgentState

RELIABILITY_PROMPT = """
You are the Reliability Investigator in an enterprise log analysis system.
Analyze candidate events for:
- application failures
- exceptions
- database failures
- HTTP 5xx errors
- connection failures
- service failures
- timeouts
- crashes

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
If no meaningful reliability issue exists:

{"findings": []}
"""
def reliability_agent(state: AgentState) -> AgentState:
    candidates = state.get("candidates", [])
    evidence = state.get("evidence", [])
    reliability_candidates = [
        candidate
        for candidate in candidates
        if candidate.get("type") in {"repeated_error", "error_spike"}
    ]
    if not reliability_candidates:
        return {"reliability_findings": []}
    relevant_evidence = [
        item for item in evidence if item.get("candidate") in reliability_candidates
    ]
    prompt = f"""
{RELIABILITY_PROMPT}
Candidate events:
{json.dumps(reliability_candidates, indent=2)}
Supporting log evidence:
{json.dumps(relevant_evidence, indent=2)}
"""
    response = llm.invoke(prompt)
    try:
        result = json.loads(response.content)
    except json.JSONDecodeError:
        result = {"findings": []}
    return {"reliability_findings": result.get("findings", [])}
