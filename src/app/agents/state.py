from typing import Any, TypedDict
from app.schemas.log_event import LogEvent
class AgentState(TypedDict, total=False):
    file_id: str
    filename: str
    events: list[LogEvent]
    candidates: list[dict[str, Any]]
    evidence: list[dict[str, Any]]
    selected_agent: str
    security_findings: list[dict[str, Any]]
    reliability_findings: list[dict[str, Any]]
    performance_findings: list[dict[str, Any]]
    combined_findings: list[dict[str, Any]]
    rag_context: str
    rag_citations: list[dict[str, Any]]
    internal_context: list[dict[str, Any]]
    github_context: list[dict[str, Any]]
    gmail_context: list[dict[str, Any]]
    rca: dict[str, Any]
    validated_findings: list[dict[str, Any]]
    final_report: dict[str, Any]
    evaluation_question: str
    evaluation_reference: str
    ragas_evaluation: dict[str, Any]
