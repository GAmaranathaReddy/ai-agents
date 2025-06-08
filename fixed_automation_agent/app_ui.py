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
        Interact with the Fixed Automation Agent. This agent responds to specific commands
        based on its predefined rules.

        **Available commands:**
        - `hello` (or `hi`, `hey`)
        - `about`
        - `add X Y` (e.g., `add 10 5`)
        - `multiply X Y` (e.g., `multiply 7 3`)
    """)

    # User input
    with st.form(key="command_form"):
        user_input = st.text_input(
            "Enter your command:",
            placeholder="e.g., 'add 5 3' or 'hello'",
            key="user_command"
        )
        submit_button = st.form_submit_button(label="Send Command")

    if submit_button and user_input:
        st.markdown("---")
        agent = st.session_state.fixed_agent # Use the agent from session state

        with st.spinner("Agent processing..."):
            agent_response = agent.process_request(user_input) # Use process_request as per automation.py

        # Display the response
        st.subheader("Agent's Response:")
        st.write(agent_response)
        st.markdown("---")

    elif submit_button and not user_input:
        st.warning("Please enter a command.")

    st.sidebar.header("About This Agent")
    st.sidebar.info(
        f"This is the '{st.session_state.fixed_agent.name}'. "
        "It demonstrates the Fixed Automation Agent pattern, where an agent follows a "
        "strict set of programmed rules to respond to specific inputs."
    )
    st.sidebar.markdown("---")
    st.sidebar.subheader("Example Valid Inputs")
    st.sidebar.code("hello\nadd 10 20\nmultiply 3 8\nabout")

if __name__ == "__main__":
    main()
