from __future__ import annotations
from mcp import Client, StdioServerParameters
class MCPClient:
    def __init__(
        self, command: str, args: list[str], env: dict[str, str] | None = None
    ):
        self.server = StdioServerParameters(command=command, args=args, env=env)
    def get_client(self) -> Client:
        return Client(self.server)
