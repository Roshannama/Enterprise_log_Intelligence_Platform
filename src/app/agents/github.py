from app.agents.state import AgentState
from app.mcp.github_tools import (
    github_search_code,
    github_search_issues,
    github_search_pull_requests,
)


async def github_context_agent(state: AgentState) -> AgentState:
    findings = state.get("combined_findings", [])
    github_context = []
    for finding in findings:
        category = finding.get("category", "").lower()
        if category not in {
            "database_failure",
            "application_error",
            "api_failure",
            "performance",
            "reliability",
        }:
            continue
        title = finding.get("title", "")
        description = finding.get("description", "")
        query = f"{title} {description}".strip()
        if not query:
            continue
        try:
            issue_result = await github_search_issues(query=query)
            github_context.append(
                {"type": "github_issue_search", "query": query, "result": issue_result}
            )
        except Exception as exc:
            github_context.append({"type": "github_error", "error": str(exc)})
    return {"github_context": github_context}
