import asyncio
from dotenv import load_dotenv
from app.mcp.github_client import create_github_client

load_dotenv()

OWNER = "Roshannama"
REPO = "cargo_project"


async def main():
    async with create_github_client() as client:
        print("Connected to GitHub MCP.")
        result = await client.call_tool(
            "get_file_contents", {"owner": OWNER, "repo": REPO, "path": "/"}
        )
        print("\nRepository contents:\n")
        for content in result.content:
            print(content)


if __name__ == "__main__":
    asyncio.run(main())
