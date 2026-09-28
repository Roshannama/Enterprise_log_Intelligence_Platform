import asyncio
from app.services.github_service import search_github_for_finding, get_github_file

OWNER = "Roshannama"
REPO = "cargo_project"


async def main():
    print("=" * 60)
    print("GITHUB SERVICE TEST")
    print("=" * 60)
    finding = {
        "title": "Password hashing implementation",
        "description": "Application uses password authentication and PBKDF2",
        "category": "security",
    }
    print("\n[1] Searching GitHub for finding...")
    context = await search_github_for_finding(finding)
    print("\nQuery:")
    print(context["query"])
    print("\n--- CODE ---")
    print(context["code"][:3000])
    print("\n--- ISSUES ---")
    print(context["issues"][:3000])
    print("\n--- PULL REQUESTS ---")
    print(context["pull_requests"][:3000])
    print("\n[2] Reading README.md...")
    file_context = await get_github_file(owner=OWNER, repo=REPO, path="README.md")
    print("\n--- README ---")
    print(file_context["content"][:3000])
    print("\n")
    print("=" * 60)
    print("GITHUB SERVICE TEST COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
