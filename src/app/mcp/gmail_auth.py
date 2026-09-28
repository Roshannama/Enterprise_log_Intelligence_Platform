from __future__ import annotations
from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from app.core.config import GMAIL_CREDENTIALS_FILE, GMAIL_TOKEN_FILE

GMAIL_SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.compose",
]


def get_gmail_credentials() -> Credentials:
    credentials_path = Path(GMAIL_CREDENTIALS_FILE)
    token_path = Path(GMAIL_TOKEN_FILE)
    if not credentials_path.exists():
        raise FileNotFoundError(
            f"Gmail OAuth credentials not found: " f"{credentials_path}"
        )
    credentials = None
    if token_path.exists():
        credentials = Credentials.from_authorized_user_file(
            str(token_path), GMAIL_SCOPES
        )
    if credentials and credentials.expired and credentials.refresh_token:
        credentials.refresh(Request())
    elif not credentials or not credentials.valid:
        flow = InstalledAppFlow.from_client_secrets_file(
            str(credentials_path), GMAIL_SCOPES
        )
        credentials = flow.run_local_server(port=0)
    token_path.parent.mkdir(parents=True, exist_ok=True)
    token_path.write_text(credentials.to_json(), encoding="utf-8")
    return credentials
