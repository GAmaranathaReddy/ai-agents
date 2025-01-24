import streamlit as st
from streamlit_chat import message  # For chat-like UI
from phi.agent import Agent
from phi.model.ollama import Ollama
from phi.tools.duckduckgo import DuckDuckGo

# Initialize the agent
web_agent = Agent(
    name="Web Agent",
    model=Ollama(id="llama3.2"),
    tools=[DuckDuckGo()],
    instructions=["Always include sources"],
    show_tool_calls=True,
    markdown=True,
)

# Streamlit app setup
st.set_page_config(page_title="Web Search Chatbot", page_icon="🤖", layout="centered")
st.title("🤖 Web Search Chatbot")
st.markdown("Ask the AI anything! Sources are included.")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize user input state
if "user_input" not in st.session_state:
    st.session_state.user_input = ""

# Input box and button
with st.container():
    user_input = st.text_input(
        "Your message:",
        placeholder="Type your question here...",
        key="unique_user_input",
        label_visibility="collapsed",
        value=st.session_state.user_input,  # Bind the value to session state
    )

    if st.button("Send", key="send_button"):
        if user_input.strip():
            with st.spinner("The agent is thinking..."):
                try:
                    # Get the agent's response
                    response = web_agent.run(user_input)
                    response_content = response.to_dict() if hasattr(response, "to_dict") else response.json() if hasattr(response, "json") else str(response)

                    # Append the agent's response to the chat history
                    st.session_state.messages.append({"role": "agent", "content": response_content['content']})
                    # Append the user's message to the chat history
                    st.session_state.messages.append({"role": "user", "content": user_input})
                except Exception as e:
                    st.session_state.messages.append({"role": "agent", "content": f"Error: {str(e)}"})

            # Clear input field and rerun to refresh
            st.session_state["user_input"] = ""


# Display chat history in reverse order (latest message at top)
for i, chat_message in enumerate(reversed(st.session_state.messages)):
    key = f"message_{i}"
    if chat_message["role"] == "user":
        message(chat_message["content"], is_user=True, key=key)  # User's message in chat bubble
    elif chat_message["role"] == "agent":
        message(chat_message["content"], is_user=False, key=key)  # Agent's message in chat bubble

# Add footer
st.markdown("---")
st.markdown("💡 Powered by Ollama and DuckDuckGo")
