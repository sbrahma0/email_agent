from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from typing import TypedDict
from gmail_client import fetch_latest_emails, fetch_email_content
from llm_agent import ask_llm


# --- State ---
class EmailState(TypedDict):
    messages: list  # LLM chat history
    last_email_list: list  # store latest fetched emails


# --- Node ---
def email_node(state: EmailState):
    try:
        user_input = state["messages"][-1]["content"]

        # Task 1: Fetch latest emails
        if "latest emails" in user_input.lower() or "5 latest" in user_input.lower():
            latest = fetch_latest_emails(5)
            state["last_email_list"] = latest
            reply = "Here are your latest emails:\n"
            for i, mail in enumerate(latest, 1):
                reply += f"{i}. From: {mail['sender']}, Time: {mail['time']}\n"
            state["messages"].append({"role": "assistant", "content": reply})
            return state

        # Task 2: Summarize specific email
        if "summarize email" in user_input.lower():
            import re
            match = re.search(r"email (\d+)", user_input.lower())
            if match and state.get("last_email_list"):
                idx = int(match.group(1)) - 1
                if 0 <= idx < len(state["last_email_list"]):
                    email_id = state["last_email_list"][idx]["id"]
                    content = fetch_email_content(email_id)
                    summary = ask_llm(
                        state["messages"] + [{"role": "user", "content": f"Summarize this email: {content}"}]
                    )
                    state["messages"].append({"role": "assistant", "content": summary.content})
                    return state
            state["messages"].append({"role": "assistant", "content": "⚠️ Could not find that email."})
            return state

        # Default: LLM response
        response = ask_llm(state["messages"])
        state["messages"].append({"role": "assistant", "content": response.content})
        return state

    except Exception as e:
        # Catch unexpected errors
        state["messages"].append({"role": "assistant", "content": f"⚠️ System error: {str(e)}"})
        return state


# --- Build graph ---
workflow = StateGraph(EmailState)
workflow.add_node("email_node", email_node)
workflow.set_entry_point("email_node")
workflow.add_edge("email_node", END)  # stops after one node execution
memory = MemorySaver()
app = workflow.compile(checkpointer=memory)
