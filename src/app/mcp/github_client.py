from __future__ import annotations
import os
from dotenv import load_dotenv
from mcp import Client
from app.mcp.client import MCPClient
load_dotenv()

def create_github_client() -> Client:
    token = os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")
    if not token:
        raise ValueError("GITHUB_PERSONAL_ACCESS_TOKEN is not configured.")
    mcp_client = MCPClient(
        command="docker",
        args=[
            "run",
            "-i",
            "--rm",
            "-e",
            "GITHUB_PERSONAL_ACCESS_TOKEN",
            "-e",
            "GITHUB_READ_ONLY=1",
            "ghcr.io/github/github-mcp-server",
        ],
        env={**os.environ, "GITHUB_PERSONAL_ACCESS_TOKEN": token},
    )
    return mcp_client.get_client()
