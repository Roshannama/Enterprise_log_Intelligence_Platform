import asyncio
import json
from app.agents.mcp import mcp_context_agent


async def main():
    state = {
        "security_findings": [],
        "reliability_findings": [
            {
                "category": "database_failure",
                "title": "Repeated database connection failures",
                "description": (
                    "PaymentService experienced repeated database "
                    "connection failures."
                ),
                "severity": "HIGH",
                "confidence": 0.95,
            }
        ],
        "performance_findings": [],
    }
    print("=" * 70)
    print("COMBINED MCP TEST")
    print("=" * 70)
    result = await mcp_context_agent(state)
    print("\nGITHUB CONTEXT")
    print("-" * 70)
    print(json.dumps(result.get("github_context", []), indent=2, default=str))
    print("\nGMAIL CONTEXT")
    print("-" * 70)
    print(json.dumps(result.get("gmail_context", []), indent=2, default=str))
    print("\n" + "=" * 70)
    print("MCP TEST COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())
