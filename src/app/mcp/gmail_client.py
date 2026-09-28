from __future__ import annotations
import httpx2
from mcp import Client
from mcp.client.streamable_http import streamable_http_client
from app.core.config import GMAIL_MCP_URL
from app.mcp.gmail_auth import get_gmail_credentials


class GmailMCPClient:
    def __init__(self):
        self.credentials = None
        self.http_client = None
        self.transport = None
        self.client = None
    async def __aenter__(self):
        self.credentials = get_gmail_credentials()
        access_token = self.credentials.token
        self.http_client = httpx2.AsyncClient(
            headers={
                "Authorization": (f"Bearer {access_token}"),
                "Accept": ("application/json, " "text/event-stream"),
                "Content-Type": ("application/json"),
            },
            timeout=httpx2.Timeout(30.0, read=300.0),
        )
        await self.http_client.__aenter__()
        self.transport = streamable_http_client(
            GMAIL_MCP_URL, http_client=self.http_client
        )
        self.client = Client(self.transport)
        await self.client.__aenter__()
        return self.client
    async def __aexit__(self, exc_type, exc_value, traceback):
        if self.client:
            await self.client.__aexit__(exc_type, exc_value, traceback)
        if self.http_client:
            await self.http_client.__aexit__(exc_type, exc_value, traceback)
