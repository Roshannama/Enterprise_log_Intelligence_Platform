import asyncio
from dotenv import load_dotenv
from app.mcp.github_client import create_github_client

load_dotenv()


async def main():
    print("Starting GitHub MCP client...")
    async with create_github_client() as client:
        print("Connected to GitHub MCP server.")
        print("\nServer information:")
        print(client.server_info)
        print("\nProtocol version:")
        print(client.protocol_version)
        print("\nGetting available tools...")
        response = await client.list_tools()
        print(f"\nFound {len(response.tools)} tools.\n")
        for tool in response.tools:
            print("=" * 70)
            print("Tool:", tool.name)
            print("Description:")
            print(tool.description)
            print("\nInput schema:")
            print(tool.input_schema)
    print("\nGitHub MCP connection closed.")


if __name__ == "__main__":
    asyncio.run(main())
