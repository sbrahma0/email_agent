from gmail_client import get_gmail_service


def list_labels():
    """List Gmail labels to confirm connection works."""
    service = get_gmail_service()
    results = service.users().labels().list(userId="me").execute()
    labels = results.get("labels", [])
    return [label["name"] for label in labels]


def main():
    print("🔹 Connecting to Gmail...")
    labels = list_labels()
    print("✅ Gmail Connected. Labels:", labels)


if __name__ == "__main__":
    main()
