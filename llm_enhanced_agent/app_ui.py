import streamlit as st
from agent import LLMEnhancedAgent # Assuming agent.py is in the same directory

# Initialize the agent
# We can instantiate it once and store it in session state for persistence across reruns
if 'agent' not in st.session_state:
    st.session_state.agent = LLMEnhancedAgent(llm_service_name="WebUI-LLM")

def main():
    st.set_page_config(page_title="LLM-Enhanced Agent", layout="centered")
    st.title("🤖 LLM-Enhanced Agent Interface")
    st.markdown("""
        This is a simple web interface for the LLM-Enhanced Agent.
        The agent uses a simulated LLM to process your input.
    """)

    # User input
    with st.form(key="query_form"):
        user_input = st.text_input("Enter your query or message:", placeholder="Type here...", key="user_query")
        submit_button = st.form_submit_button(label="Send to Agent")

    if submit_button and user_input:
        st.markdown("---")
        # Process the input using the agent
        # For this simple agent, re-instantiating or using a session-state agent is fine.
        # Using session state agent here:
        agent = st.session_state.agent

        with st.spinner("Agent is thinking..."):
            agent_response = agent.process_request(user_input)

        # Display the response
        st.subheader("Agent's Response:")
        st.write(agent_response) # Using st.write for potentially formatted output

        # Optionally, display "LLM's" raw contribution for clarity in this demo
        llm_raw_response = agent.get_llm_response(user_input) # Assuming get_llm_response is accessible
        st.caption(f"Simulated LLM Output: \"{llm_raw_response}\"")
        st.markdown("---")

    elif submit_button and not user_input:
        st.warning("Please enter some text for the agent.")

    st.sidebar.header("About")
    st.sidebar.info(
        "This application demonstrates the LLM-Enhanced Agent pattern. "
        "The agent's responses are enhanced by a simulated Large Language Model."
    )
    st.sidebar.markdown("---")
    st.sidebar.subheader("Agent Details")
    st.sidebar.write(f"LLM Service: {st.session_state.agent.llm_service_name}")


if __name__ == "__main__":
    main()
