import asyncio
from app.services.gmail_service import create_gmail_draft


async def main():
    result = await create_gmail_draft(
        to=["roshannama1208@gmail.com"],
        subject="Log Intelligence Test Draft",
        body=("This is a test draft generated " "by the Log Intelligence Platform."),
    )
    print("\nDraft created successfully:\n")
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
