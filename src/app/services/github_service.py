from __future__ import annotations
from typing import Any
from app.mcp.github_tools import (
    github_get_file,
    github_search_code,
    github_search_issues,
    github_search_pull_requests,
)


def _extract_text(result: Any) -> str:
    if result is None:
        return ""
    content = getattr(result, "content", None)
    if not content:
        return str(result)
    parts = []
    for item in content:
        text_value = getattr(item, "text", None)
        if text_value:
            parts.append(text_value)
    return "\n".join(parts)


def _clean_query(text: str, max_words: int = 30) -> str:
    words = text.split()
    return " ".join(words[:max_words])


async def search_github_for_finding(finding: dict[str, Any]) -> dict[str, Any]:
    title = finding.get("title", "")
    description = finding.get("description", finding.get("message", ""))
    category = finding.get("category", "")
    search_query = _clean_query(
        " ".join(part for part in [title, description, category] if part)
    )
    if not search_query:
        return {"query": "", "code": "", "issues": "", "pull_requests": ""}
    result = {
        "query": search_query,
        "code": "",
        "issues": "",
        "pull_requests": "",
        "errors": [],
    }
    try:
        code_result = await github_search_code(search_query)
        result["code"] = _extract_text(code_result)
    except Exception as exc:
        result["errors"].append(f"code search: {exc}")
    try:
        issue_result = await github_search_issues(query=search_query)
        result["issues"] = _extract_text(issue_result)
    except Exception as exc:
        result["errors"].append(f"issue search: {exc}")
    try:
        pr_result = await github_search_pull_requests(query=search_query)
        result["pull_requests"] = _extract_text(pr_result)
    except Exception as exc:
        result["errors"].append(f"pull request search: {exc}")
    return result


async def github_search_for_question(
    question: str, report: dict | None = None
) -> dict[str, Any]:
    report = report or {}
    incident = report.get("incident", "")
    rca = report.get("rca", {})
    root_cause = rca.get("potential_root_cause", "") if isinstance(rca, dict) else ""
    query_parts = [question, incident, root_cause]
    query = _clean_query(" ".join(part for part in query_parts if part))
    result = {
        "query": query,
        "code": "",
        "issues": "",
        "pull_requests": "",
        "errors": [],
    }
    try:
        result["code"] = _extract_text(await github_search_code(query))
    except Exception as exc:
        result["errors"].append(f"code search: {exc}")
    try:
        result["issues"] = _extract_text(await github_search_issues(query=query))
    except Exception as exc:
        result["errors"].append(f"issue search: {exc}")
    try:
        result["pull_requests"] = _extract_text(
            await github_search_pull_requests(query=query)
        )
    except Exception as exc:
        result["errors"].append(f"pull request search: {exc}")
    return result


async def get_github_file(
    owner: str, repo: str, path: str, ref: str | None = None
) -> dict[str, Any]:
    result = await github_get_file(owner=owner, repo=repo, path=path, ref=ref)
    return {
        "owner": owner,
        "repo": repo,
        "path": path,
        "content": _extract_text(result),
    }
