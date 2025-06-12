import streamlit as st
from agent import ReActRAGAgent # Agent now uses the common LLM client factory
from knowledge_base_manager import SAMPLE_DOCUMENTS_FOR_DB # To show available knowledge
from common.llm_providers.client import SUPPORTED_PROVIDERS, DEFAULT_PROVIDER
import os

# --- Agent Initialization Function ---
def initialize_react_agent():
    provider = st.session_state.get("react_selected_provider", os.getenv("LLM_PROVIDER", DEFAULT_PROVIDER))
    model = st.session_state.get("react_selected_model", "") # Allow empty for provider's default

    provider_kwargs = {}
    if provider == "openai": pass # Rely on env var
    elif provider == "gemini": pass # Rely on env var
    elif provider == "bedrock":
        provider_kwargs['region_name'] = st.session_state.get("react_aws_region", os.getenv("AWS_REGION"))

    try:
        # Pass model_name specifically, let agent's __init__ handle fallbacks if it's empty
        agent_instance = ReActRAGAgent(provider_name=provider, model_name=model if model else None, **provider_kwargs)
        st.session_state.react_rag_agent = agent_instance
        st.session_state.react_agent_error = None
        st.success(f"ReAct+RAG Agent initialized with {agent_instance.name}")
    except Exception as e:
        st.session_state.react_rag_agent = None
        st.session_state.react_agent_error = f"Failed to initialize ReActRAGAgent: {e}"
        st.error(st.session_state.react_agent_error)

# --- UI Rendering ---
def main():
    st.set_page_config(page_title="ReAct+RAG Agent", layout="wide")
    st.title("🧠 ReAct + RAG Agent Interface (Multi-Provider)")

    # --- Sidebar for Configuration ---
    st.sidebar.header("LLM Configuration for ReAct+RAG Agent")

    provider_options = list(SUPPORTED_PROVIDERS.keys())
    selected_provider = st.sidebar.selectbox(
        "Choose LLM Provider:",
        options=provider_options,
        index=provider_options.index(st.session_state.get("react_selected_provider", os.getenv("LLM_PROVIDER", DEFAULT_PROVIDER))),
        key="react_selected_provider_widget",
        on_change=lambda: st.session_state.update(react_selected_provider=st.session_state.react_selected_provider_widget)
    )
    st.session_state.react_selected_provider = selected_provider

    # Determine a sensible default model based on the provider selected
    default_model_for_provider = "mistral" # General default
    if selected_provider == "openai": default_model_for_provider = "gpt-3.5-turbo-1106" # Good at JSON
    elif selected_provider == "gemini": default_model_for_provider = "gemini-pro"
    elif selected_provider == "bedrock": default_model_for_provider = "anthropic.claude-3-sonnet-20240229-v1:0"

    selected_model = st.sidebar.text_input(
        "Enter Model Name (Ensure it's good at JSON & reasoning):",
        value=st.session_state.get("react_selected_model", default_model_for_provider),
        key="react_selected_model_widget",
        on_change=lambda: st.session_state.update(react_selected_model=st.session_state.react_selected_model_widget)
    )
    st.session_state.react_selected_model = selected_model

    if selected_provider == "bedrock":
        st.sidebar.text_input("AWS Region (Optional, uses AWS_REGION env var or default config)",
                              value=st.session_state.get("react_aws_region", os.getenv("AWS_REGION","")),
                              key="react_aws_region_widget",
                              on_change=lambda: st.session_state.update(react_aws_region=st.session_state.react_aws_region_widget)
                              )
        st.session_state.react_aws_region = st.session_state.react_aws_region_widget


    if st.sidebar.button("Initialize/Update ReAct Agent", key="init_react_agent_button"):
        initialize_react_agent()

    st.sidebar.markdown("---")
    st.sidebar.header("About This Agent")
    if st.session_state.get('react_rag_agent'):
        st.sidebar.info(
            f"This is '{st.session_state.react_rag_agent.name}'. It uses an LLM for reasoning (to decide if retrieval is needed and what to search for) "
            "and for synthesizing answers from retrieved knowledge (from ChromaDB) and user queries. "
            "Both reasoning and synthesis steps use the configured LLM."
        )
        st.sidebar.markdown(f"Currently using: **{st.session_state.react_rag_agent.actual_provider_name} / {st.session_state.react_rag_agent.llm_model}**")
    elif st.session_state.get("react_agent_error"):
         st.sidebar.error(st.session_state.react_agent_error)

    st.sidebar.markdown("---")
    st.sidebar.subheader("Knowledge Base Contents (Sample IDs):")
    st.sidebar.markdown("The agent can retrieve information about these topics from ChromaDB:")
    kb_ids = [doc['id'] for doc in SAMPLE_DOCUMENTS_FOR_DB]
    st.sidebar.code(f"{', '.join(kb_ids)}")


    # --- Main Chat Interface ---
    st.markdown(f"""
        Interact with the ReAct+RAG agent. Provider: **{selected_provider.capitalize()}**.
        Model: **{selected_model or 'Default'}**.
    """)
    st.markdown("Ensure the selected provider is configured (Ollama running, API keys for cloud services set in your environment).")


    if 'react_rag_agent' not in st.session_state and not st.session_state.get('react_agent_error'):
        initialize_react_agent()

    if st.session_state.get('react_rag_agent'):
        agent = st.session_state.react_rag_agent
        # User input form
        with st.form(key="query_form_react_rag"):
            user_input = st.text_input(
                "Enter your query:",
                placeholder="e.g., 'tell me about python', 'what is RAG?', 'doc1'",
                key="user_query_react_rag"
            )
            submit_button = st.form_submit_button(label="Submit to Agent")

        if submit_button and user_input:
            st.markdown("---")
            with st.spinner(f"{agent.name} is reasoning and acting..."):
                results = agent.reason_and_act(user_input)

            st.subheader("Agent's Process & Response:")

            if results.get("thought_process"):
                with st.expander("View Agent's Thought Process", expanded=True): # Expand by default
                    for i, thought in enumerate(results["thought_process"]):
                        st.markdown(f"_{i+1}. {thought}_")

            if results.get("action_taken"):
                st.markdown(f"**Action/Phase:** `{results['action_taken']}`")
            if results.get("query_for_retrieval"):
                st.markdown(f"**Query for Retrieval:** `{results['query_for_retrieval']}`")

            retrieved = results.get("retrieved_info")
            if retrieved:
                st.markdown("**Retrieved Information:**")
                st.info(retrieved)
            elif "Retrieval" in results.get("action_taken", ""): # If retrieval was attempted but nothing found
                 st.warning("Retrieval action was part of the plan, but no specific information was found or returned from the knowledge base.")

            st.markdown("**Final Response:**")
            st.success(results.get("final_response", "No final response generated."))
            st.markdown("---")

        elif submit_button and not user_input:
            st.warning("Please enter a query for the agent.")
    else:
        st.error("ReAct+RAG Agent could not be initialized. Please check configurations in the sidebar and ensure the selected LLM provider is operational.")

if __name__ == "__main__":


if __name__ == "__main__":
    main()
