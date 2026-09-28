import asyncio
from dotenv import load_dotenv
from app.mcp.github_client import create_github_client

load_dotenv()


async def main():
    async with create_github_client() as client:
        print("Connected to GitHub MCP.")
        result = await client.call_tool("get_me", {})
        print("\nAuthenticated GitHub user:\n")
        for content in result.content:
            print(content)


if __name__ == "__main__":
    asyncio.run(main())
