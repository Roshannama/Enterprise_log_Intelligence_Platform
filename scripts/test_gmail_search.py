import asyncio
from app.mcp.gmail_tools import gmail_search_threads


async def main():
    result = await gmail_search_threads(query="newer_than:30d", page_size=5)
    print("\nGmail search result:\n")
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
