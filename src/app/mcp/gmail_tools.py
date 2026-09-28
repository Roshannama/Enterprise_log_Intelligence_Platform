from __future__ import annotations
from typing import Any
from app.mcp.manager import mcp_manager


def _structured_result(result: Any) -> Any:
    structured = getattr(result, "structured_content", None)
    if structured is not None:
        return structured
    content = getattr(result, "content", None)
    if not content:
        return result
    text_parts = []
    for item in content:
        text_value = getattr(item, "text", None)
        if text_value:
            text_parts.append(text_value)
    return "\n".join(text_parts)


async def gmail_search_threads(query: str, page_size: int = 10):
    client = mcp_manager.get_gmail_client()
    async with client as session:
        result = await session.call_tool(
            "search_threads",
            {
                "query": query,
                "pageSize": min(page_size, 50),
                "view": "THREAD_VIEW_MINIMAL",
            },
        )
        return _structured_result(result)


async def gmail_get_thread(thread_id: str):
    client = mcp_manager.get_gmail_client()
    async with client as session:
        result = await session.call_tool(
            "get_thread", {"threadId": thread_id, "messageFormat": "FULL_CONTENT"}
        )
        return _structured_result(result)


async def gmail_create_draft(
    to: list[str],
    subject: str,
    body: str,
    cc: list[str] | None = None,
    bcc: list[str] | None = None,
    reply_to_message_id: str | None = None,
):
    client = mcp_manager.get_gmail_client()
    arguments = {"to": to, "subject": subject, "body": body}
    if cc:
        arguments["cc"] = cc
    if bcc:
        arguments["bcc"] = bcc
    if reply_to_message_id:
        arguments["replyToMessageId"] = reply_to_message_id
    async with client as session:
        result = await session.call_tool("create_draft", arguments)
        return _structured_result(result)
