from gmail_client import get_gmail_service
from llm_agent import ask_llm


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

    # Example: ask the LLM to explain Gmail labels
    user_prompt = (
        f"I connected to Gmail and got these labels: {labels}. "
        "Explain what they mean and how they can be useful."
    )
    llm_response = ask_llm(user_prompt)
    print("\n🤖 LLM says:\n", llm_response)


if __name__ == "__main__":
    main()
