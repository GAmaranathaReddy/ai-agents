import streamlit as st
from agent import LLMEnhancedAgent # Agent now uses the common LLM client factory
from common.llm_providers.client import SUPPORTED_PROVIDERS, DEFAULT_PROVIDER
import os

# --- Agent Initialization Function ---
def initialize_agent():
    provider = st.session_state.get("selected_provider", os.getenv("LLM_PROVIDER", DEFAULT_PROVIDER))
    model = st.session_state.get("selected_model", "") # Allow empty if using provider's default

    # Provider-specific kwargs (API keys, region)
    provider_kwargs = {}
    if provider == "openai":
        # OpenAI client will look for OPENAI_API_KEY env var if api_key is not passed
        # provider_kwargs['api_key'] = st.session_state.get("openai_api_key", os.getenv("OPENAI_API_KEY"))
        pass # Rely on env var or pre-configured client
    elif provider == "gemini":
        # provider_kwargs['api_key'] = st.session_state.get("google_api_key", os.getenv("GOOGLE_API_KEY"))
        pass # Rely on env var
    elif provider == "bedrock":
        provider_kwargs['region_name'] = st.session_state.get("aws_region", os.getenv("AWS_REGION"))

    try:
        agent_instance = LLMEnhancedAgent(provider_name=provider, model_name=model if model else None, **provider_kwargs)
        st.session_state.agent = agent_instance
        st.session_state.agent_error = None # Clear previous errors
        st.success(f"Agent initialized with {agent_instance.llm_service_name}")
    except Exception as e:
        st.session_state.agent = None
        st.session_state.agent_error = f"Failed to initialize agent: {e}"
        st.error(st.session_state.agent_error)

# --- UI Rendering ---
def main():
    st.set_page_config(page_title="LLM-Enhanced Agent", layout="centered")
    st.title("🤖 LLM-Enhanced Agent Interface")

    # --- Sidebar for Configuration ---
    st.sidebar.header("LLM Configuration")

    # Provider selection
    provider_options = list(SUPPORTED_PROVIDERS.keys())
    selected_provider = st.sidebar.selectbox(
        "Choose LLM Provider:",
        options=provider_options,
        index=provider_options.index(st.session_state.get("selected_provider", os.getenv("LLM_PROVIDER", DEFAULT_PROVIDER))),
        key="selected_provider_widget", # Use a different key for widget to avoid conflict with direct session_state set
        on_change=lambda: st.session_state.update(selected_provider=st.session_state.selected_provider_widget)
    )
    st.session_state.selected_provider = selected_provider


    # Model name input
    default_model_for_provider = ""
    if selected_provider == "ollama": default_model_for_provider = "mistral"
    elif selected_provider == "openai": default_model_for_provider = "gpt-3.5-turbo"
    elif selected_provider == "gemini": default_model_for_provider = "gemini-pro"
    elif selected_provider == "bedrock": default_model_for_provider = "anthropic.claude-3-sonnet-20240229-v1:0"

    selected_model = st.sidebar.text_input(
        "Enter Model Name (or leave blank for provider's default/agent's default):",
        value=st.session_state.get("selected_model", default_model_for_provider),
        key="selected_model_widget",
        on_change=lambda: st.session_state.update(selected_model=st.session_state.selected_model_widget)
    )
    st.session_state.selected_model = selected_model


    # API Key / Region specific inputs (optional, as env vars are primary)
    if selected_provider == "openai":
        st.sidebar.text_input("OpenAI API Key (Optional, uses OPENAI_API_KEY env var if not set)", type="password", key="openai_api_key")
    elif selected_provider == "gemini":
        st.sidebar.text_input("Google API Key (Optional, uses GOOGLE_API_KEY env var if not set)", type="password", key="google_api_key")
    elif selected_provider == "bedrock":
        st.sidebar.text_input("AWS Region (Optional, uses AWS_REGION env var or default config)", key="aws_region")

    if st.sidebar.button("Initialize/Update Agent", key="init_agent_button"):
        initialize_agent()

    st.sidebar.markdown("---")
    st.sidebar.header("About")
    st.sidebar.info(
        "This application demonstrates the LLM-Enhanced Agent pattern using a common "
        "abstraction layer to interact with various LLM providers."
    )
    if st.session_state.get("agent"):
        st.sidebar.markdown("---")
        st.sidebar.subheader("Current Agent Details")
        st.sidebar.write(f"Provider/Model: `{st.session_state.agent.llm_service_name}`")
    elif st.session_state.get("agent_error"):
         st.sidebar.error(st.session_state.agent_error)


    # --- Main Chat Interface ---
    st.markdown(f"""
        This interface now uses the **`{st.session_state.get("selected_provider", DEFAULT_PROVIDER).capitalize()}`** provider.
        {(f"Model: **`{st.session_state.get('selected_model', 'Default')}`**" if st.session_state.get('selected_model') else "Using provider's default model.")}
        Please ensure the chosen provider is correctly configured (e.g., Ollama running, API keys set for cloud providers).
    """)

    # Initialize agent on first run if not already initialized by button
    if 'agent' not in st.session_state and not st.session_state.get('agent_error'):
        initialize_agent()

    if st.session_state.get('agent'):
        agent = st.session_state.agent
        # User input form
        with st.form(key="query_form"):
            user_input = st.text_input("Enter your query or message:", placeholder="Type here...", key="user_query")
            submit_button = st.form_submit_button(label="Send to Agent")

        if submit_button and user_input:
            st.markdown("---")
            with st.spinner(f"{agent.name} is thinking..."):
                agent_response = agent.process_request(user_input)

            st.subheader("Agent's Response:")
            st.markdown(agent_response) # Using markdown for better formatting potential
            st.markdown("---")

        elif submit_button and not user_input:
            st.warning("Please enter some text for the agent.")
    else:
        st.error("Agent could not be initialized. Please check configurations in the sidebar and ensure the selected LLM provider is operational.")


if __name__ == "__main__":


if __name__ == "__main__":
    main()
