import json
from app.agents.llm import llm
from app.agents.state import AgentState

SECURITY_PROMPT = """
You are the Security Investigator in an enterprise log analysis system.
Analyze the provided candidate log events ONLY for security-related issues.
Look for:
- credential or secret exposure
- authentication failures
- authorization problems
- suspicious access
- sensitive information exposure
- possible injection indicators
Do not invent evidence.
Return JSON with this structure:

{
  "findings": [
    {
      "category": "...",
      "title": "...",
      "severity": "LOW|MEDIUM|HIGH|CRITICAL",
      "description": "...",
      "evidence": "...",
      "potential_impact": "...",
      "confidence": 0.0
    }
  ]
}
If there is no meaningful security issue, return:

{"findings": []}
"""


def security_agent(state: AgentState) -> AgentState:
    candidates = state.get("candidates", [])
    evidence = state.get("evidence", [])
    security_candidates = [
        candidate
        for candidate in candidates
        if candidate.get("type") == "potential_security_issue"
    ]
    if not security_candidates:
        return {"security_findings": []}
    relevant_evidence = [
        item for item in evidence if item.get("candidate") in security_candidates
    ]
    prompt = f"""
{SECURITY_PROMPT}

Candidate events:

{json.dumps(security_candidates, indent=2)}

Supporting log evidence:

{json.dumps(relevant_evidence, indent=2)}
"""
    response = llm.invoke(prompt)
    try:
        result = json.loads(response.content)
    except json.JSONDecodeError:
        result = {"findings": []}
    return {"security_findings": result.get("findings", [])}
