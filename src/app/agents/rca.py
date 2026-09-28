from __future__ import annotations
import json
from app.agents.json_utils import parse_llm_json
from app.agents.llm import llm
from app.agents.state import AgentState

RCA_PROMPT = """
You are the Correlation and Root Cause Investigator
for an enterprise log intelligence platform.
You receive:
1. Direct log evidence.
2. Security findings.
3. Reliability findings.
4. Performance findings.
5. Internal MCP log context.
6. RAG knowledge.
7. GitHub repository context.
8. Gmail operational context.

Your job is to:

1. Identify findings that belong to the same incident.
2. Connect related symptoms.
3. Determine the most evidence-supported potential root cause.
4. Distinguish observed evidence from documentation.
5. Distinguish repository evidence from operational context.
6. Identify hypotheses explicitly.
7. Never claim a root cause is proven unless
   direct evidence supports it.

SOURCE DEFINITIONS:

DIRECT LOG EVIDENCE:
Evidence actually present in the uploaded log.

INTERNAL MCP:
Additional retrieval from the uploaded log and
service metadata.

RAG:
Documentation, runbooks, policies, historical
knowledge or other reference material.

GITHUB:
Repository, code, issue and pull-request context.

GMAIL:
Operational email context.

IMPORTANT:

RAG documentation does NOT prove that an incident
occurred.

GitHub results do NOT prove that a code change
caused an incident.

Gmail messages do NOT prove a root cause unless
their contents directly establish it.

Return JSON only:

{
  "incident": "...",
  "related_findings": [],
  "potential_root_cause": "...",
  "reasoning": "...",
  "confidence": 0.0
}
"""


def _get_findings(state: AgentState) -> list[dict]:
    findings: list[dict] = []
    findings.extend(state.get("security_findings", []))
    findings.extend(state.get("reliability_findings", []))
    findings.extend(state.get("performance_findings", []))
    return findings


def rca_agent(state: AgentState) -> AgentState:
    findings = _get_findings(state)
    if not findings:
        return {"combined_findings": [], "rca": {}}
    rag_context = state.get("rag_context", "")
    rag_citations = state.get("rag_citations", [])
    internal_context = state.get("internal_context", [])
    github_context = state.get("github_context", [])
    gmail_context = state.get("gmail_context", [])
    prompt = f"""
{RCA_PROMPT}

SPECIALIZED FINDINGS

{json.dumps(
    findings,
    indent=2,
    default=str,
)}

RAG KNOWLEDGE

{rag_context}

RAG CITATIONS

{json.dumps(
    rag_citations,
    indent=2,
    default=str,
)}

INTERNAL MCP CONTEXT

{json.dumps(
    internal_context,
    indent=2,
    default=str,
)}

GITHUB MCP CONTEXT

{json.dumps(
    github_context,
    indent=2,
    default=str,
)}

GMAIL MCP CONTEXT

{json.dumps(
    gmail_context,
    indent=2,
    default=str,
)}

REASONING RULES

Separate:

- direct log evidence
- internal MCP evidence
- documented knowledge
- repository evidence
- operational context
- hypothesis

Do not convert a documented possibility into
a confirmed root cause.

Return only valid JSON.
"""
    response = llm.invoke(prompt)
    try:
        rca_result = parse_llm_json(response.content)
    except ValueError:
        rca_result = {
            "incident": "Unable to determine",
            "related_findings": [],
            "potential_root_cause": None,
            "reasoning": ("RCA response could not " "be parsed."),
            "confidence": 0.0,
        }
    return {"combined_findings": findings, "rca": rca_result}
