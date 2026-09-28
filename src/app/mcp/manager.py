from __future__ import annotations
from app.mcp.github_client import create_github_client
from app.mcp.gmail_client import GmailMCPClient


class MCPManager:
    def get_github_client(self):
        return create_github_client()
    def get_gmail_client(self):
        return GmailMCPClient()


mcp_manager = MCPManager()
