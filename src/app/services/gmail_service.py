from __future__ import annotations
from typing import Any
from app.mcp.gmail_tools import (
    gmail_create_draft,
    gmail_get_thread,
    gmail_search_threads,
)


def _build_gmail_query(finding: dict[str, Any]) -> str:
    title = str(finding.get("title", "")).strip()
    description = str(finding.get("description", "")).strip()
    category = str(finding.get("category", "")).strip()
    if title:
        words = title.split()
        return " ".join(words[:8])
    if description:
        words = description.split()
        return " ".join(words[:8])
    return category


async def search_gmail_for_finding(finding: dict[str, Any]) -> dict[str, Any]:
    query = _build_gmail_query(finding)
    if not query:
        return {"query": "", "threads": []}
    result = await gmail_search_threads(query=query, page_size=5)
    return {"query": query, "threads": result}


async def search_gmail_for_question(
    question: str, report: dict | None = None
) -> dict[str, Any]:
    report = report or {}
    incident = str(report.get("incident", ""))
    query_parts = [question, incident]
    query = " ".join(part for part in query_parts if part)
    query = " ".join(query.split()[:20])
    result = await gmail_search_threads(query=query, page_size=10)
    return {"query": query, "threads": result}


async def get_gmail_thread(thread_id: str) -> dict[str, Any]:
    result = await gmail_get_thread(thread_id)
    return {"thread_id": thread_id, "thread": result}


async def create_gmail_draft(
    to: list[str],
    subject: str,
    body: str,
    cc: list[str] | None = None,
    bcc: list[str] | None = None,
    reply_to_message_id: str | None = None,
) -> Any:
    return await gmail_create_draft(
        to=to,
        subject=subject,
        body=body,
        cc=cc,
        bcc=bcc,
        reply_to_message_id=(reply_to_message_id),
    )
