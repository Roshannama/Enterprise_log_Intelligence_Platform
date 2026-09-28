from __future__ import annotations
from app.agents.state import AgentState
from app.rag.pipeline import retrieve_knowledge


def _get_findings(state: AgentState) -> list[dict]:
    findings: list[dict] = []
    findings.extend(state.get("security_findings", []))
    findings.extend(state.get("reliability_findings", []))
    findings.extend(state.get("performance_findings", []))
    return findings


def rag_agent(state: AgentState) -> AgentState:
    findings = _get_findings(state)
    if not findings:
        return {"rag_context": "", "rag_citations": []}
    finding_text = []
    for finding in findings:
        finding_text.append(f"""
Title: {finding.get("title", "")}
Category: {finding.get("category", "")}
Description: {finding.get("description", "")}
Potential Impact: {finding.get("potential_impact", "")}
Potential Root Cause: {finding.get("potential_root_cause", "")}
""".strip())
    query = "\n\n".join(finding_text)
    try:
        result = retrieve_knowledge(
            query=query,
            dense_k=10,
            sparse_k=10,
            rerank_k=8,
            final_k=5,
            relevance_threshold=0.50,
        )
        return {
            "rag_context": result.get("context", ""),
            "rag_citations": result.get("citations", []),
        }
    except Exception as exc:
        return {"rag_context": ("RAG retrieval failed: " f"{exc}"), "rag_citations": []}
