import streamlit as st
from agent import ToolEnhancedAgent # Assuming agent.py is in the same directory

# Initialize the agent
if 'tool_agent' not in st.session_state:
    st.session_state.tool_agent = ToolEnhancedAgent()

def main():
    st.set_page_config(page_title="Tool-Enhanced Agent", layout="wide")
    st.title("🛠️ Tool-Enhanced Agent Interface")
    st.markdown("""
        Interact with an agent that uses an **LLM (via Ollama)** to understand your natural language query
        and select the appropriate tool (like getting time, summing numbers, or checking weather).
    """)

    # User input
    with st.form(key="query_form_tool_enhanced"):
        user_input = st.text_input(
            "Enter your query in natural language:",
            placeholder="e.g., 'What's the time?', 'Sum 15 and 8', 'How is the weather in Berlin?'",
            key="user_query_tool_enhanced"
        )
        submit_button = st.form_submit_button(label="Send to Agent")

    if submit_button and user_input:
        st.markdown("---")
        agent = st.session_state.tool_agent

        with st.spinner("Agent and LLM processing your request..."):
            results = agent.process_request(user_input) # This now returns a more detailed dict

        st.subheader("Agent's Processing Details & Response:")

        st.markdown(f"**You asked:** \"{results.get('user_input', '')}\"")

        # Display LLM Interpretation
        if results.get("llm_interpretation"):
            with st.expander("View LLM Interpretation (Tool Selection & Arguments)", expanded=False):
                st.json(results["llm_interpretation"])

        if results.get('tool_used') and results['tool_used'] != "unknown":
            st.markdown(f"**Tool Selected by LLM:** `{results['tool_used']}`")
            if results.get('tool_input_params'):
                st.markdown(f"**Tool Input Parameters (from LLM):** `{results['tool_input_params']}`")

            if results.get('tool_output_raw'):
                st.markdown("**Tool's Direct Output:**")
                st.info(str(results['tool_output_raw'])) # Ensure it's a string for display
        elif results.get('tool_used') == "unknown":
            st.info("LLM determined no specific tool was suitable for your request.")
        else: # Should not happen if llm_interpretation was successful but no tool_used
            st.warning("LLM did not select a specific tool or 'unknown'.")


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
        f"This is '{st.session_state.tool_agent.name}'. It uses an LLM "
        "to understand natural language and decide which internal tool "
        "(like date/time, sum calculator, weather) to use and what arguments to pass to it."
    )
    st.sidebar.markdown("---")
    st.sidebar.subheader("Available Tools & Example Natural Language Commands:")
    st.sidebar.markdown("""
    - **Get Current Datetime**:
      - `What time is it right now?`
      - `Tell me the current date.`
    - **Calculate Sum**:
      - `What is 123 plus 456?`
      - `Can you sum 10.5 and 22.3 for me?`
    - **Get Weather (Simulated)**:
      - `How's the weather in London?`
      - `weather for Paris please`
    - *The agent will try to map other queries to 'unknown'.*
    """)

if __name__ == "__main__":
    main()
