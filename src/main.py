from email_agent_graph import app

if __name__ == "__main__":
    print("💬 Email Agent (multi-turn) started. Type 'exit' to quit.\n")
    thread = {"configurable": {"thread_id": "email-thread"}}
    state = {"messages": [], "last_email_list": []}

    while True:
        user_input = input("You: ")
        if user_input.lower() in {"exit", "quit"}:
            print("👋 Goodbye!")
            break

        state["messages"].append({"role": "user", "content": user_input})
        state = app.invoke(state, config=thread)
        output = state["messages"][-1]["content"]
        print("Assistant:", output)