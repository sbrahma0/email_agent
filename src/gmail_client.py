import os
import pickle
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials


SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]


def get_gmail_service():
    """Authenticate and return a Gmail service object."""
    creds = None
    base_dir = os.path.dirname(os.path.dirname(__file__))  # project root
    token_path = os.path.join(base_dir, "token.json")
    creds_path = os.path.join(base_dir, "credentials.json")

    # Load saved token
    if os.path.exists(token_path):
        with open(token_path, "rb") as token:
            creds = pickle.load(token)

    # If no valid credentials, refresh or run OAuth flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                creds_path, SCOPES
            )
            creds = flow.run_local_server(port=0)

        # Save for next time
        with open(token_path, "wb") as token:
            pickle.dump(creds, token)

    return build("gmail", "v1", credentials=creds)


def fetch_latest_emails(n=5):
    """Fetch latest n emails. Returns a list of dicts with 'id', 'sender', 'time'."""
    # Connect to Gmail and fetch messages
    # Return list of dicts: [{'id': 'xxx', 'sender': 'John Doe', 'time': 'Thu ...'}, ...]
    pass


def fetch_email_content(email_id):
    """Return the plain text or snippet of a specific email by ID."""
    pass


