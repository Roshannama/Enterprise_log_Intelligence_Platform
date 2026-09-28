from __future__ import annotations
import json
import re
from pathlib import Path
from typing import Any
from app.agents.json_utils import parse_llm_json
from app.agents.llm import llm
from app.rag.pipeline import retrieve_knowledge
from app.mcp.tools.log_tools import get_log_context, search_logs
from app.mcp.tools.service_tools import get_service_metadata
from app.services.github_service import github_search_for_question
from app.services.gmail_service import create_gmail_draft, search_gmail_for_question

CHAT_SYSTEM_PROMPT = """
You are an enterprise log investigation assistant.

You have access to:

1. Investigation report
2. Uploaded log evidence
3. Internal Log MCP
4. RAG knowledge
5. GitHub MCP
6. Gmail MCP

SOURCE RULES:

Investigation report:
Generated analysis of the uploaded investigation.

Uploaded logs:
Direct evidence from the uploaded file.

Internal Log MCP:
Additional retrieval from the uploaded log and
service metadata.

RAG:
Documentation, runbooks, policies, historical
knowledge and reference material.

GitHub MCP:
Repository code, issues and pull requests.

Gmail MCP:
Operational email and thread context.

IMPORTANT:

Never invent evidence.

Never claim that RAG documentation proves that
an incident occurred.

Never claim that GitHub proves a root cause
unless the returned repository evidence directly
supports it.

Never claim that Gmail proves a root cause
unless the returned email content directly
supports it.

When information is unavailable, say so.

When useful, explicitly identify the source.

Keep answers concise and technically useful.
"""


def _safe_json(value: Any) -> str:
    try:
        return json.dumps(value, indent=2, default=str)
    except Exception:
        return str(value)


def _contains_any(text: str, keywords: list[str]) -> bool:
    lowered = text.lower()
    return any(keyword.lower() in lowered for keyword in keywords)


def _extract_email(text: str) -> str | None:
    match = re.search(r"[\w.+-]+@[\w-]+\.[\w.-]+", text)
    if match:
        return match.group(0)
    return None


def _is_github_question(question: str) -> bool:
    return _contains_any(
        question,
        [
            "github",
            "repository",
            "repo",
            "issue",
            "issues",
            "pull request",
            "pull requests",
            "commit",
            "code change",
            "source code",
        ],
    )


def _is_gmail_question(question: str) -> bool:
    return _contains_any(
        question, ["gmail", "email", "emails", "mail", "thread", "threads", "inbox"]
    )


def _is_draft_request(question: str) -> bool:
    return _contains_any(
        question,
        [
            "create a gmail draft",
            "create an email draft",
            "write a gmail draft",
            "write an email draft",
            "draft an email",
            "draft a gmail",
            "create a draft",
        ],
    )


def _build_internal_queries(question: str, report: dict) -> list[str]:
    queries: list[str] = []
    if question:
        queries.append(question)
    incident = report.get("incident", "")
    if incident:
        queries.append(str(incident))
    findings = report.get("findings", [])
    if isinstance(findings, list):
        for finding in findings[:5]:
            if not isinstance(finding, dict):
                continue
            for key in ["title", "message", "description", "category"]:
                value = finding.get(key, "")
                if value:
                    queries.append(str(value))
    rca = report.get("rca", {})
    if isinstance(rca, dict):
        root_cause = rca.get("potential_root_cause", "")
        if root_cause:
            queries.append(str(root_cause))
    unique = []
    for query in queries:
        query = " ".join(query.split())
        if not query:
            continue
        if query not in unique:
            unique.append(query[:300])
    return unique[:5]


async def _retrieve_internal_context(
    question: str, report: dict, file_id: str, filename: str
) -> dict[str, Any]:
    if not file_id or not filename:
        return {
            "available": False,
            "reason": ("Uploaded file information " "is unavailable."),
        }
    extension = Path(filename).suffix.lower()
    stored_filename = f"{file_id}{extension}"
    result: dict[str, Any] = {
        "available": True,
        "source": "internal_log_mcp",
        "filename": filename,
        "stored_filename": stored_filename,
        "queries": [],
        "log_matches": [],
        "log_context": [],
        "service_metadata": {},
    }
    queries = _build_internal_queries(question=question, report=report)
    result["queries"] = queries
    seen_event_ids: set[str] = set()
    for query in queries:
        try:
            matches = search_logs(filename=stored_filename, query=query, limit=10)
        except Exception as exc:
            result.setdefault("errors", []).append(f"Log search failed: {exc}")
            continue
        for event in matches:
            event_id = event.get("event_id")
            if event_id in seen_event_ids:
                continue
            if event_id:
                seen_event_ids.add(event_id)
            result["log_matches"].append(event)
    for event in result["log_matches"][:5]:
        event_id = event.get("event_id")
        if not event_id:
            continue
        try:
            context = get_log_context(
                filename=stored_filename, event_id=event_id, window=2
            )
            result["log_context"].append({"event_id": event_id, "events": context})
        except Exception as exc:
            result.setdefault("errors", []).append(f"Context lookup failed: {exc}")
    try:
        result["service_metadata"] = get_service_metadata(filename=stored_filename)
    except Exception as exc:
        result["service_metadata_error"] = str(exc)
    return result


async def _create_requested_gmail_draft(question: str, report: dict) -> dict[str, Any]:
    recipient = _extract_email(question)
    if not recipient:
        return {
            "success": False,
            "answer": ("Please provide a valid " "recipient email address."),
        }
    prompt = f"""
You are preparing a professional Gmail draft
for an enterprise incident investigation.

Create an email summarizing the investigation.

Recipient:
{recipient}

Investigation report:
{json.dumps(
    report,
    indent=2,
    default=str,
)}

Return ONLY valid JSON:

{{
    "subject": "...",
    "body": "..."
}}
"""
    response = llm.invoke(prompt)
    try:
        draft = parse_llm_json(response.content)
    except ValueError:
        return {
            "success": False,
            "answer": ("I could not generate a valid " "email draft."),
        }
    subject = str(draft.get("subject", "Incident Investigation Summary"))
    body = str(draft.get("body", ""))
    if not body:
        return {"success": False, "answer": ("The generated email body " "was empty.")}
    try:
        gmail_result = await create_gmail_draft(
            to=[recipient], subject=subject, body=body
        )
        return {
            "success": True,
            "answer": (f"Gmail draft created for " f"{recipient}."),
            "recipient": recipient,
            "subject": subject,
            "body": body,
            "gmail_result": gmail_result,
        }
    except Exception as exc:
        return {
            "success": False,
            "answer": ("The Gmail draft could not " f"be created: {exc}"),
        }


async def answer_question(
    report: dict, question: str, file_id: str = "", filename: str = ""
) -> dict[str, Any]:
    question = question.strip()
    if not question:
        return {"answer": ("Please enter a question."), "sources": [], "tool_calls": []}
    if _is_draft_request(question):
        draft_result = await _create_requested_gmail_draft(
            question=question, report=report
        )
        return {
            "answer": draft_result["answer"],
            "sources": [{"type": "gmail_mcp", "source": "Gmail create_draft"}],
            "tool_calls": ["Gmail MCP: create_draft"],
            "draft": draft_result,
        }
    context: dict[str, Any] = {}
    sources: list[dict[str, Any]] = []
    tool_calls: list[str] = []
    context["investigation_report"] = report
    sources.append(
        {"type": "investigation_report", "source": "stored investigation report"}
    )
    try:
        rag_query = f"""
User question:
{question}

Investigation:
{_safe_json(report)}
"""
        rag_result = retrieve_knowledge(
            query=rag_query,
            dense_k=10,
            sparse_k=10,
            rerank_k=8,
            final_k=5,
            relevance_threshold=0.50,
        )
        context["rag"] = {
            "context": rag_result.get("context", ""),
            "citations": rag_result.get("citations", []),
        }
        tool_calls.append("RAG")
        for citation in rag_result.get("citations", []):
            sources.append({"type": "rag", **citation})
    except Exception as exc:
        context["rag_error"] = str(exc)
    try:
        internal_context = await _retrieve_internal_context(
            question=question, report=report, file_id=file_id, filename=filename
        )
        context["internal_log_mcp"] = internal_context
        tool_calls.append("Internal Log MCP")
        sources.append({"type": "internal_mcp", "source": filename})
    except Exception as exc:
        context["internal_mcp_error"] = str(exc)
    if _is_github_question(question):
        try:
            github_result = await github_search_for_question(
                question=question, report=report
            )
            context["github_mcp"] = github_result
            tool_calls.append("GitHub MCP")
            sources.append({"type": "github_mcp", "source": "GitHub"})
        except Exception as exc:
            context["github_mcp_error"] = str(exc)
    if _is_gmail_question(question):
        try:
            gmail_result = await search_gmail_for_question(
                question=question, report=report
            )
            context["gmail_mcp"] = gmail_result
            tool_calls.append("Gmail MCP")
            sources.append({"type": "gmail_mcp", "source": "Gmail"})
        except Exception as exc:
            context["gmail_mcp_error"] = str(exc)
    prompt = f"""
{CHAT_SYSTEM_PROMPT}

USER QUESTION

{question}

AVAILABLE CONTEXT

{_safe_json(context)}

ANSWERING RULES

Answer the user's question using the
available evidence.

Prefer direct log evidence when discussing
what actually happened.

Use RAG for documentation and recommendations.

Use GitHub only when repository evidence is
available.

Use Gmail only when email evidence is
available.

If a tool returned no useful result, say so.

Do not invent missing information.

Clearly distinguish:

Observed:
What the logs actually show.

Documented:
What the RAG knowledge says.

External context:
What GitHub or Gmail contains.

Hypothesis:
What may explain the incident.

Do not claim a hypothesis is proven.

FINAL ANSWER
"""
    response = llm.invoke(prompt)
    return {"answer": response.content, "sources": sources, "tool_calls": tool_calls}
