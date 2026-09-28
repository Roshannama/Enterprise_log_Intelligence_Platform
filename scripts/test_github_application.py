import asyncio
from dotenv import load_dotenv
from app.mcp.github_tools import github_get_file, github_search_code

load_dotenv()

OWNER = "Roshannama"
REPO = "cargo_project"


async def main():
    print("\nTesting GitHub application integration...\n")
    result = await github_get_file(owner=OWNER, repo=REPO, path="README.md")
    print("README result:")
    print(result)
    print("\nTesting code search...\n")
    result = await github_search_code(query=f"repo:{OWNER}/{REPO}")
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
