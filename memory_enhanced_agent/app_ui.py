import streamlit as st
from agent import MemoryEnhancedAgent # Assuming agent.py is in the same directory

# Initialize agent and chat history in session state
if 'memory_agent' not in st.session_state:
    st.session_state.memory_agent = MemoryEnhancedAgent()
    # agent_name = st.session_state.memory_agent.name # Get agent name after init
    # st.session_state.memory_agent_name = agent_name # Store it if needed elsewhere

if 'chat_ui_history' not in st.session_state:
    st.session_state.chat_ui_history = [] # Stores tuples of (speaker, message) for UI display

def display_chat_message(speaker: str, message: str, is_user: bool):
    if is_user:
        st.markdown(f"<div style='text-align: right; margin-bottom: 10px;'><span style='background-color: #DCF8C6; color: #000; border-radius: 10px; padding: 8px 12px; display: inline-block; max-width: 70%;'>{message}</span><br><small style='color: #555; text-align: right;'>You</small></div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div style='text-align: left; margin-bottom: 10px;'><span style='background-color: #E0E0E0; color: #000; border-radius: 10px; padding: 8px 12px; display: inline-block; max-width: 70%;'>{message}</span><br><small style='color: #555;'>{st.session_state.memory_agent.name}</small></div>", unsafe_allow_html=True)


def main():
    st.set_page_config(page_title="Memory-Enhanced Agent Chat", layout="centered")
    st.title(f"💬 Chat with {st.session_state.memory_agent.name}")
    st.markdown("This agent can remember your name, preferences, and past parts of this conversation.")

    # Chat display area
    chat_container = st.container()
    with chat_container:
        for speaker, message in st.session_state.chat_ui_history:
            display_chat_message(speaker, message, speaker == "User")
        st.markdown("<div id='bottom_anchor'></div>", unsafe_allow_html=True) # Anchor for scrolling

    # Input form - using a simpler approach than st.form for chat
    user_input = st.chat_input("Say something to the agent...")

    if user_input:
        # Add user message to UI history and display it immediately
        st.session_state.chat_ui_history.append(("User", user_input))

        # Process with agent
        agent_response = st.session_state.memory_agent.chat(user_input)

        # Add agent response to UI history
        st.session_state.chat_ui_history.append((st.session_state.memory_agent.name, agent_response))

        # Rerun to update the chat display and clear input
        st.experimental_rerun()


    # Sidebar to display memory
    st.sidebar.header("Agent's Memory")
    if st.sidebar.button("Refresh Memory View"):
        st.sidebar.experimental_rerun() # To get latest memory after interaction

    with st.sidebar.expander("🧠 Learned Facts", expanded=False):
        facts = st.session_state.memory_agent.memory.get_all_facts()
        if facts:
            st.json(facts)
        else:
            st.info("No facts learned yet.")

    with st.sidebar.expander("📜 Agent's Internal Conversation Log", expanded=False):
        internal_history = st.session_state.memory_agent.memory.get_conversation_history()
        if internal_history:
            for i, (user_turn, agent_turn) in enumerate(internal_history):
                st.text(f"Turn {i+1}:")
                st.text(f"  {user_turn}")
                st.text(f"  {agent_turn}")
        else:
            st.info("No interactions logged in agent's internal history yet.")

    st.sidebar.markdown("---")
    st.sidebar.subheader("Example Interactions")
    st.sidebar.code("""
User: Hello, my name is Alice.
Agent: Nice to meet you, Alice! How can I help you today?
User: I like the color red.
Agent: Noted, Alice! Your favorite color is red.
User: What is my favorite color?
Agent: Alice, your favorite color is red.
    """)


if __name__ == "__main__":
    main()
