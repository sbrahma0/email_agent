import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def ask_llm(
    prompt: str,
    system_prompt: str = "You are a helpful assistant."
) -> str:
    """
    Send a prompt to Groq LLM and return the response text.

    Args:
        prompt (str): The user's question or instruction.
        system_prompt (str, optional): System instructions for LLM behavior.

    Returns:
        str: LLM's response, or fallback message if something goes wrong.
    """
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
        )

        # Extract response content safely
        if response.choices and response.choices[0].message:
            return response.choices[0].message.content.strip()
        else:
            return "[LLM returned no content]"

    except Exception as e:
        # Catch API/network errors
        return f"[Error communicating with LLM: {e}]"
