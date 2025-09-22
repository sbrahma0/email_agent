import os
import pickle
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import base64
from email import message_from_bytes

SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]


def get_gmail_service():
    """Authenticate and return a Gmail service object."""
    creds = None
    base_dir = os.path.dirname(os.path.dirname(__file__))  # project root
    token_path = os.path.join(base_dir, "token.json")
    creds_path = os.path.join(base_dir, "credentials.json")

    if os.path.exists(token_path):
        with open(token_path, "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                creds_path, SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open(token_path, "wb") as token:
            pickle.dump(creds, token)

    return build("gmail", "v1", credentials=creds)


# ------------------- Gmail Tasks -------------------
service = get_gmail_service()


def fetch_latest_emails(n=5):
    """Fetch latest n emails. Returns list of dicts with 'id', 'sender', 'time'."""
    results = service.users().messages().list(userId="me", maxResults=n, labelIds=['INBOX']).execute()
    messages = results.get("messages", [])

    emails = []
    for m in messages:
        msg = service.users().messages().get(userId="me", id=m["id"], format="metadata", metadataHeaders=["From", "Date"]).execute()
        headers = msg.get("payload", {}).get("headers", [])
        sender = next((h["value"] for h in headers if h["name"] == "From"), "Unknown")
        date = next((h["value"] for h in headers if h["name"] == "Date"), "Unknown")
        emails.append({"id": m["id"], "sender": sender, "time": date})

    return emails


def fetch_email_content(email_id):
    """Return the plain text content of a specific email by ID."""
    msg = service.users().messages().get(userId="me", id=email_id, format="raw").execute()
    raw_data = base64.urlsafe_b64decode(msg["raw"].encode("ASCII"))
    email_msg = message_from_bytes(raw_data)

    # Get the email body (plain text)
    if email_msg.is_multipart():
        for part in email_msg.walk():
            if part.get_content_type() == "text/plain":
                return part.get_payload(decode=True).decode("utf-8", errors="ignore")
    else:
        return email_msg.get_payload(decode=True).decode("utf-8", errors="ignore")

    return ""
