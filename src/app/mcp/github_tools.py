from __future__ import annotations
from typing import Any
from app.mcp.manager import mcp_manager


async def github_get_file(
    owner: str, repo: str, path: str = "/", ref: str | None = None
) -> Any:
    client = mcp_manager.get_github_client()
    arguments = {"owner": owner, "repo": repo, "path": path}
    if ref:
        arguments["ref"] = ref
    async with client as session:
        result = await session.call_tool("get_file_contents", arguments)
        return result


async def github_search_code(query: str) -> Any:
    client = mcp_manager.get_github_client()
    async with client as session:
        result = await session.call_tool("search_code", {"query": query})
        return result


async def github_search_issues(
    query: str, owner: str | None = None, repo: str | None = None
) -> Any:
    client = mcp_manager.get_github_client()
    arguments = {"query": query}
    if owner:
        arguments["owner"] = owner
    if repo:
        arguments["repo"] = repo
    async with client as session:
        result = await session.call_tool("search_issues", arguments)
        return result


async def github_search_pull_requests(
    query: str, owner: str | None = None, repo: str | None = None
) -> Any:
    client = mcp_manager.get_github_client()
    arguments = {"query": query}
    if owner:
        arguments["owner"] = owner
    if repo:
        arguments["repo"] = repo
    async with client as session:
        result = await session.call_tool("search_pull_requests", arguments)
        return result
