import streamlit as st
from agent import SelfReflectingAgent # Assuming agent.py is in the same directory

# Initialize the agent
if 'self_reflecting_agent' not in st.session_state:
    st.session_state.self_reflecting_agent = SelfReflectingAgent()

def main():
    st.set_page_config(page_title="Self-Reflecting Agent", layout="wide")
    st.title("🧐 Self-Reflecting Agent Interface")
    st.markdown("""
        Interact with an agent that attempts a task, critiques its own work, and then tries to refine it.
        Enter a prompt for a task (e.g., writing a short story, making a simple plan).
    """)

    # User input
    with st.form(key="prompt_form_self_reflecting"):
        user_prompt = st.text_input(
            "Enter your prompt for the agent:",
            placeholder="e.g., 'write a story about a dog', 'plan a trip to the beach'",
            key="user_prompt_self_reflecting"
        )
        submit_button = st.form_submit_button(label="Process Prompt")

    if submit_button and user_prompt:
        st.markdown("---")
        agent = st.session_state.self_reflecting_agent

        with st.spinner("Agent is working and reflecting..."):
            results = agent.process_request(user_prompt)

        st.subheader("Agent's Self-Reflection Process:")

        # Display Initial Output
        st.markdown("**1. Initial Output:**")
        st.info(results.get("initial_output", "N/A"))

        # Display Critique
        st.markdown("**2. Critique:**")
        critique = results.get("critique", "N/A")
        if critique == "No critique.":
            st.success(critique)
        else:
            st.warning(critique)

        # Display Refined Output (if any)
        refined_output = results.get("refined_output")
        initial_output = results.get("initial_output")

        if critique != "No critique.":
            st.markdown("**3. Refined Output:**")
            if refined_output and refined_output != initial_output:
                st.info(refined_output)
            elif refined_output and refined_output == initial_output:
                 st.info(f"(Agent attempted refinement, but the output remained the same: \"{refined_output}\")")
            else: # This case should ideally not happen if critique was present and refinement was attempted
                st.info("(No distinct refined output was generated despite critique.)")

        st.markdown("---")
        st.subheader("Agent's Final Output:")
        st.success(results.get("final_output", "N/A"))
        st.markdown("---")

        # Optional: Display full log for debugging or deeper insight
        with st.expander("View Agent's Internal Log", expanded=False):
            for log_entry in results.get("log", []):
                st.text(log_entry)

    elif submit_button and not user_prompt:
        st.warning("Please enter a prompt for the agent.")

    # Sidebar for information
    st.sidebar.header("About This Agent")
    st.sidebar.info(
        f"This is '{st.session_state.self_reflecting_agent.name}'. It demonstrates a basic "
        "self-reflection loop: generate an initial output, critique that output based on "
        "simple rules, and then attempt to refine the output based on the critique."
    )
    st.sidebar.markdown("---")
    st.sidebar.subheader("Example Prompts:")
    st.sidebar.code("""
- write a story about a cat
- plan a trip to Paris
- code a python hello world
- write a story about a dog
- plan a trip to the beach
    """)
    st.sidebar.markdown(
        "The agent's critique and refinement capabilities are based on simple predefined rules "
        "in `critique_mechanism.py` and `task_performer.py`."
    )

if __name__ == "__main__":
    main()
