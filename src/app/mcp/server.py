from mcp.server import MCPServer
from app.mcp.tools.log_tools import get_log_context, search_logs
from app.mcp.tools.service_tools import get_service_metadata

mcp = MCPServer("Log Intelligence MCP Server")


@mcp.tool(description=("Search uploaded log files for events " "matching a query."))
def search_logs_tool(filename: str, query: str, limit: int = 10) -> list[dict]:
    return search_logs(filename=filename, query=query, limit=limit)


@mcp.tool(description=("Retrieve log events surrounding a " "specific event ID."))
def get_log_context_tool(filename: str, event_id: str, window: int = 2) -> list[dict]:
    return get_log_context(filename=filename, event_id=event_id, window=window)


@mcp.tool(
    description=(
        "Return basic metadata and severity " "statistics for a service in a log file."
    )
)
def get_service_metadata_tool(filename: str, service: str | None = None) -> dict:
    return get_service_metadata(filename=filename, service=service)
