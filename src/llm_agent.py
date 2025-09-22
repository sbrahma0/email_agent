import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain.schema import AIMessage, BaseMessage

load_dotenv()

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY")
)


def ask_llm(messages: list) -> BaseMessage:
    """Send a multi-turn message list to Groq LLM and return its response.
    Handles API errors gracefully and returns an error message if it fails."""
    try:
        response = llm.invoke(messages)
        return response
    except Exception as e:
        # Return a message in the same format
        return AIMessage(content=f"⚠️ Unable to get LLM response: {str(e)}")
