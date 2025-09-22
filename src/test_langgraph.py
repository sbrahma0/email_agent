from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_groq import ChatGroq
from typing import TypedDict
import os
from dotenv import load_dotenv

# --- Load env ---
load_dotenv()

# --- Groq client ---
llm = ChatGroq(
    model="llama-3.1-8b-instant",   # fast + free tier friendly
    api_key=os.getenv("GROQ_API_KEY")
)


# --- State ---
class ChatState(TypedDict):
    messages: list


# --- Node function ---
def chat_node(state: ChatState):
    response = llm.invoke(state["messages"])
    return {"messages": state["messages"] + [response]}


# --- Build graph ---
workflow = StateGraph(ChatState)
workflow.add_node("chat", chat_node)
workflow.set_entry_point("chat")
workflow.add_edge("chat", END)

# --- Memory ---
memory = MemorySaver()
app = workflow.compile(checkpointer=memory)

# --- Interactive loop ---
if __name__ == "__main__":
    thread = {"configurable": {"thread_id": "demo-thread"}}
    print("💬 Multi-turn chatbot started (Groq). Type 'exit' to quit.\n")

    state = {"messages": []}

    while True:
        user_input = input("You: ")
        if user_input.lower() in {"exit", "quit"}:
            break

        state["messages"].append({"role": "user", "content": user_input})
        result = app.invoke(state, config=thread)
        ai_msg = result["messages"][-1].content
        print("Assistant:", ai_msg)
