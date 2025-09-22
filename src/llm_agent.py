import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain.schema import AIMessage


load_dotenv()

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY")
)


def ask_llm(messages: list) -> AIMessage:
    """Send a multi-turn message list to Groq LLM and return its response.
    Handles API errors gracefully and informs the user."""
    try:
        response = llm.invoke(messages)
        return response
    except Exception as e:  # catch all LLM/API errors
        msg = str(e)
        if "quota" in msg.lower() or "token" in msg.lower() or "limit" in msg.lower():
            friendly_msg = "⚠️ LLM cannot process your request: your API token may be exhausted or quota exceeded. Please wait or refresh the token."
        else:
            friendly_msg = f"⚠️ LLM encountered an error: {msg}"
        from langchain.schema import AIMessage
        return AIMessage(content=friendly_msg)