import asyncio
import json
from app.mcp.gmail_tools import gmail_search_threads


async def main():
    print("=" * 70)
    print("GMAIL MCP CONNECTION TEST")
    print("=" * 70)
    try:
        print("\n[1] Searching Gmail...")
        result = await gmail_search_threads(query="newer_than:30d", page_size=5)
        print("\n[2] Gmail MCP response:")
        print("-" * 70)
        if isinstance(result, (dict, list)):
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(result)
        print("-" * 70)
        print("\nGmail MCP connection is working.")
    except Exception as e:
        print("\nGmail MCP test FAILED.")
        print(f"Error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
