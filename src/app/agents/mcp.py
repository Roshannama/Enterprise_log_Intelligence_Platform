from __future__ import annotations
from typing import Any
from app.agents.state import AgentState
from app.services.github_service import search_github_for_finding
from app.services.gmail_service import search_gmail_for_finding
from app.services.internal_mcp_service import search_internal_logs_for_finding

def _get_findings(state: AgentState) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    findings.extend(state.get("security_findings", []))
    findings.extend(state.get("reliability_findings", []))
    findings.extend(state.get("performance_findings", []))
    return findings

async def mcp_context_agent(state: AgentState) -> AgentState:
    findings = _get_findings(state)
    file_id = state.get("file_id", "")
    filename = state.get("filename", "")
    internal_context: list[dict[str, Any]] = []
    github_context: list[dict[str, Any]] = []
    gmail_context: list[dict[str, Any]] = []
    for finding in findings:
        title = finding.get("title", "")
        try:
            internal_result = await search_internal_logs_for_finding(
                finding=finding, file_id=file_id, filename=filename
            )
            internal_context.append({"finding_title": title, "result": internal_result})
        except Exception as exc:
            internal_context.append({"finding_title": title, "error": str(exc)})
        try:
            github_result = await search_github_for_finding(finding)
            if github_result.get("query"):
                github_context.append(
                    {
                        "finding_title": title,
                        "query": github_result.get("query", ""),
                        "code": github_result.get("code", ""),
                        "issues": github_result.get("issues", ""),
                        "pull_requests": github_result.get("pull_requests", ""),
                    }
                )
        except Exception as exc:
            github_context.append({"finding_title": title, "error": str(exc)})
        try:
            gmail_result = await search_gmail_for_finding(finding)
            if gmail_result.get("query"):
                gmail_context.append(
                    {
                        "finding_title": title,
                        "query": gmail_result.get("query", ""),
                        "threads": gmail_result.get("threads", []),
                    }
                )
        except Exception as exc:
            gmail_context.append({"finding_title": title, "error": str(exc)})
    return {
        "internal_context": internal_context,
        "github_context": github_context,
        "gmail_context": gmail_context,
    }
