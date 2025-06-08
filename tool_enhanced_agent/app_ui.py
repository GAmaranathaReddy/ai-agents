import streamlit as st
from agent import ToolEnhancedAgent # Assuming agent.py is in the same directory

# Initialize the agent
if 'tool_agent' not in st.session_state:
    st.session_state.tool_agent = ToolEnhancedAgent()

def main():
    st.set_page_config(page_title="Tool-Enhanced Agent", layout="wide")
    st.title("🛠️ Tool-Enhanced Agent Interface")
    st.markdown("""
        Interact with an agent that can use various tools to answer your queries.
        The agent will show which tool (if any) it used and the outcome.
    """)

    # User input
    with st.form(key="query_form_tool_enhanced"):
        user_input = st.text_input(
            "Enter your query:",
            placeholder="e.g., 'What time is it?', 'sum 10 and 5', 'weather in London'",
            key="user_query_tool_enhanced"
        )
        submit_button = st.form_submit_button(label="Send to Agent")

    if submit_button and user_input:
        st.markdown("---")
        agent = st.session_state.tool_agent

        with st.spinner("Agent is processing your request..."):
            results = agent.process_request(user_input)

        st.subheader("Agent's Processing Details & Response:")

        st.markdown(f"**You asked:** \"{results.get('user_input', '')}\"")

        if results.get('tool_used'):
            st.markdown(f"**Tool Used:** `{results['tool_used']}`")
            if results.get('tool_input_params'):
                st.markdown(f"**Tool Input Parameters:** `{results['tool_input_params']}`")
            if results.get('tool_output_raw'):
                # For tools like get_weather or calculate_sum, the "raw" output is already the final human-readable string.
                # If tools returned raw data (e.g. JSON), we might format it differently here.
                st.markdown("**Tool's Direct Output:**")
                st.info(results['tool_output_raw'])
        else:
            st.markdown("**Tool Used:** `None`")

        if results.get('error'):
            st.error(f"**Error during processing:** {results['error']}")

        st.markdown("**Agent's Final Response:**")
        st.success(results.get("final_response", "No final response generated."))

        st.markdown("---")

    elif submit_button and not user_input:
        st.warning("Please enter a query for the agent.")

    # Sidebar for information
    st.sidebar.header("About This Agent")
    st.sidebar.info(
        f"This is '{st.session_state.tool_agent.name}'. It demonstrates how an agent can "
        "select and use different 'tools' (functions) based on the user's input "
        "to provide more specific answers or perform actions."
    )
    st.sidebar.markdown("---")
    st.sidebar.subheader("Available Tools & Example Commands:")
    st.sidebar.markdown("""
    - **Get Current Datetime**:
      - `what time is it?`
      - `current date`
    - **Calculate Sum**:
      - `sum of 10 and 20`
      - `add 5 plus 3`
    - **Get Weather (Simulated)**:
      - `weather in London`
      - `what's the weather for Paris`
    """)

if __name__ == "__main__":
    main()
