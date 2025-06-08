import streamlit as st
from agent import ReActRAGAgent # Assuming agent.py is in the same directory
from knowledge_base import DOCUMENTS, STRUCTURED_DOCUMENTS # To show available knowledge

# Initialize the agent
if 'react_rag_agent' not in st.session_state:
    st.session_state.react_rag_agent = ReActRAGAgent()

def main():
    st.set_page_config(page_title="ReAct+RAG Agent", layout="wide")
    st.title("🧠 ReAct + RAG Agent Interface")
    st.markdown("""
        Interact with an agent that uses the **ReAct (Reason+Act)** and **RAG (Retrieval Augmented Generation)** patterns.
        The agent will show its thought process, any actions taken (like retrieving documents), and the final response.
    """)

    # User input
    with st.form(key="query_form_react_rag"):
        user_input = st.text_input(
            "Enter your query:",
            placeholder="e.g., 'tell me about python', 'what is RAG?', 'doc1'",
            key="user_query_react_rag"
        )
        submit_button = st.form_submit_button(label="Submit to Agent")

    if submit_button and user_input:
        st.markdown("---")
        agent = st.session_state.react_rag_agent

        with st.spinner("Agent is reasoning and acting..."):
            results = agent.reason_and_act(user_input)

        st.subheader("Agent's Process & Response:")

        # Display Thought Process
        if results.get("thought_process"):
            with st.expander("View Agent's Thought Process", expanded=False):
                for i, thought in enumerate(results["thought_process"]):
                    st.text(f"Step {i+1}: {thought}")

        # Display Action Taken and Retrieval
        if results.get("action_taken"):
            st.markdown(f"**Action Taken:** `{results['action_taken']}`")
            if results.get("query_for_retrieval"):
                st.markdown(f"**Query for Retrieval:** `{results['query_for_retrieval']}`")
            if results.get("retrieved_info"):
                st.markdown("**Retrieved Information (Snippet):**")
                st.info(f"{results['retrieved_info'][:500]}...") # Show a snippet
            elif "retrieve" in results["action_taken"]:
                 st.warning("Retrieval action was taken, but no information was found or returned.")

        # Display Final Response
        st.markdown("**Final Response:**")
        st.success(results.get("final_response", "No final response generated."))

        st.markdown("---")

    elif submit_button and not user_input:
        st.warning("Please enter a query for the agent.")

    # Sidebar for information
    st.sidebar.header("About This Agent")
    st.sidebar.info(
        f"This is '{st.session_state.react_rag_agent.name}'. It uses a ReAct (Reason+Act) loop "
        "to decide if it needs to retrieve information using RAG (Retrieval Augmented Generation) "
        "from a knowledge base before answering your query."
    )
    st.sidebar.markdown("---")
    st.sidebar.subheader("Available Knowledge Topics (Keywords):")
    st.sidebar.markdown("You can ask directly about these terms or use them in sentences like 'tell me about...'.")

    # Display available knowledge from knowledge_base.py
    simple_keys = list(DOCUMENTS.keys())
    structured_ids = [doc['id'] for doc in STRUCTURED_DOCUMENTS]
    st.sidebar.code(f"Simple KB: {', '.join(simple_keys)}")
    st.sidebar.code(f"Structured KB IDs: {', '.join(structured_ids)}")
    st.sidebar.markdown("The agent also tries to find these keywords within longer questions.")


if __name__ == "__main__":
    main()
