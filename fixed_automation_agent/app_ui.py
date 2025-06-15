import streamlit as st
from automation import FixedAutomationAgent # Assuming automation.py is in the same directory

# Initialize the agent
# Store the agent in session state for persistence across reruns
if 'fixed_agent' not in st.session_state:
    st.session_state.fixed_agent = FixedAutomationAgent()

def main():
    st.set_page_config(page_title="Fixed Automation Agent", layout="centered")
    st.title("⚙️ Fixed Automation Agent Interface")
    st.markdown("""
        Interact with the Fixed Automation Agent. This agent now uses an **LLM (via Ollama)**
        to understand natural language commands and map them to its predefined tasks.

        **You can try things like:**
        - `Hello there!`
        - `Tell me about yourself.`
        - `What is 15 plus 7?`
        - `Can you multiply 8 and 6 for me?`
    """)

    # User input
    with st.form(key="command_form"):
        user_input = st.text_input(
            "Enter your command in natural language:",
            placeholder="e.g., 'what is 5 added to 3?' or 'say hi'",
            key="user_command"
        )
        submit_button = st.form_submit_button(label="Send Command")

    if submit_button and user_input:
        st.markdown("---")
        agent = st.session_state.fixed_agent # Use the agent from session state

        with st.spinner("Agent and LLM processing..."):
            # process_request now returns a dictionary
            response_payload = agent.process_request(user_input)

        st.subheader("LLM Interpretation:")
        if response_payload.get("llm_interpretation"):
            st.json(response_payload["llm_interpretation"])
        elif response_payload.get("error") and "LLM output was not valid JSON" in response_payload["error"]:
            st.warning(f"LLM did not return valid JSON. Raw output might be in agent's error log if available, or was: {response_payload.get('llm_interpretation', 'Not captured')}")
        else:
            st.info("No detailed LLM interpretation available (or an error occurred before this stage).")

        if response_payload.get("error"):
            st.error(f"Processing Error: {response_payload['error']}")

        st.subheader("Agent's Final Result:")
        st.success(response_payload.get("final_result", "No result generated."))
        st.markdown("---")

    elif submit_button and not user_input:
        st.warning("Please enter a command.")

    st.sidebar.header("About This Agent")
    st.sidebar.info(
        f"This is '{st.session_state.fixed_agent.name}'. "
        "It uses an LLM to understand natural language and map it to one of its fixed capabilities: "
        "greeting, providing information about itself, adding two numbers, or multiplying two numbers."
    )
    st.sidebar.markdown("---")
    st.sidebar.subheader("Example Natural Language Inputs:")
    st.sidebar.code("""
Hello
Tell me about this agent
What is 25 plus 75?
Calculate the sum of 10 and 5.3
Multiply 9 by 3
what is 2 times 12
    """)

if __name__ == "__main__":
    main()
