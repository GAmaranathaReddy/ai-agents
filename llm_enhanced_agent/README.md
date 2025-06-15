# LLM-Enhanced Agent

## LLM-Enhanced Agent Pattern

The LLM-Enhanced Agent pattern involves integrating a Large Language Model (LLM) into an agent's decision-making or response-generation process. Instead of relying solely on pre-programmed logic or rules, the agent leverages the LLM's capabilities (e.g., natural language understanding, generation, reasoning) to handle more complex tasks, understand nuanced user inputs, or provide more human-like and contextually aware responses.

The core idea is to use the LLM as a "cognitive core" or a specialized component that the main agent system can query. The agent prepares the input for the LLM, calls the LLM, and then processes the LLM's output to fit the overall task or conversation.

This pattern allows developers to build more sophisticated and flexible agents by combining the strengths of traditional software engineering with the power of modern LLMs.

## Implementation

This project demonstrates the LLM-Enhanced Agent pattern by using the **common LLM abstraction layer** created in `common/llm_providers/`. This allows the agent to dynamically switch between various LLM providers (Ollama, OpenAI, Gemini, AWS Bedrock).

1.  **`common/llm_providers/` (Abstraction Layer)**:
    *   `base.py`: Defines an abstract `LLMProvider` class with `chat()` and `generate()` methods.
    *   `ollama_provider.py`, `openai_provider.py`, `gemini_provider.py`, `bedrock_provider.py`: Concrete implementations of `LLMProvider` for these specific services.
    *   `client.py`: Contains the factory function `get_llm_client(provider_name, **kwargs)` which instantiates and returns the requested provider. It can be configured via arguments or environment variables (e.g., `LLM_PROVIDER`, and provider-specific API keys).

2.  **`llm_enhanced_agent/agent.py` (`LLMEnhancedAgent` class - Refactored)**:
    *   No longer directly imports specific LLM clients (e.g., `ollama`).
    *   Its `__init__(provider_name, model_name, **provider_kwargs)` method now:
        *   Calls `get_llm_client(provider_name, **provider_kwargs)` from the common abstraction layer to obtain an `LLMProvider` instance. `provider_kwargs` can pass API keys or other necessary parameters for provider initialization.
        *   Stores this `llm_client`.
        *   Determines and stores the `model_name` to be used for its calls. This can be passed during initialization, or the agent can fall back to a default model specific to the chosen provider (e.g., "mistral" for Ollama, "gpt-3.5-turbo" for OpenAI).
    *   The `get_llm_response(user_input)` method now uses `self.llm_client.chat(model=self.model_name, messages=...)` to interact with the selected LLM provider, making the agent's core logic independent of the specific LLM service.
    *   The `process_request(user_input)` method remains the orchestrator, using the response from `get_llm_response`.

3.  **`llm_enhanced_agent/app_ui.py` (Streamlit UI - Enhanced)**:
    *   The Streamlit UI has been significantly enhanced to allow dynamic selection of the LLM provider and model.
    *   Users can choose from supported providers (Ollama, OpenAI, Gemini, Bedrock) via a sidebar dropdown.
    *   Users can specify a model name for the selected provider.
    *   The UI re-initializes the `LLMEnhancedAgent` with the chosen provider and model when these selections are made or updated.
    *   It displays the currently active provider and model.
    *   The sidebar includes notes about API key requirements for cloud-based providers (OpenAI, Gemini, Bedrock).

4.  **`llm_enhanced_agent/main.py` (CLI)**:
    *   The CLI version now also uses the `get_llm_client` factory. It will typically be configured using environment variables:
        *   `LLM_PROVIDER`: Specifies the provider (e.g., "ollama", "openai"). Defaults to "ollama".
        *   `LLM_MODEL`: Specifies the model name for the chosen provider.
        *   Provider-specific API keys/config (e.g., `OPENAI_API_KEY`, `GOOGLE_API_KEY`, AWS credentials for Bedrock).

The "enhancement" by the LLM is now highly flexible, allowing users to easily switch between different local or cloud-based LLMs through a unified agent interface and common abstraction layer.

## Prerequisites for Running

1.  **Install Python Dependencies**:
    Install all necessary Python packages listed in `llm_enhanced_agent/requirements.txt`. This file now includes `streamlit` and client libraries for all supported providers: `ollama`, `openai`, `google-generativeai`, and `boto3`.
    ```bash
    pip install -r llm_enhanced_agent/requirements.txt
    ```
    Alternatively, if you are managing dependencies for a larger project using Poetry, ensure these are added to your `pyproject.toml`.

2.  **LLM Provider Setup (Essential for the chosen provider)**:
    You need to set up at least one LLM provider to use this agent.

    *   **Ollama (Local Setup)**:
        *   Install Ollama: Refer to the [Ollama official website](https://ollama.com/).
        *   Ensure the Ollama application/service is running.
        *   Pull a model: e.g., `ollama pull mistral`. The agent often defaults to "mistral" if Ollama is selected without a specific model.

    *   **OpenAI (Cloud Setup)**:
        *   Set the `OPENAI_API_KEY` environment variable with your valid OpenAI API key.
        *   The agent often defaults to "gpt-3.5-turbo" for OpenAI if no model is specified.

    *   **Google Gemini (Cloud Setup)**:
        *   Set the `GOOGLE_API_KEY` environment variable with your Google API key (from Google AI Studio or a GCP project with the Generative Language API enabled).
        *   The agent often defaults to "gemini-pro" for Gemini.

    *   **AWS Bedrock (Cloud Setup)**:
        *   Configure your AWS credentials correctly (e.g., via `aws configure` command, IAM roles, or environment variables like `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_SESSION_TOKEN`).
        *   Set your default AWS region or pass `region_name` if initializing the Bedrock provider directly.
        *   Ensure you have model access granted for the desired Bedrock models in your AWS account for that region. The agent might default to a model like "anthropic.claude-3-sonnet-20240229-v1:0".

## How to Run

### 1. Command-Line Interface (CLI)

1.  **Configure Environment for CLI (Optional but recommended for non-Ollama providers)**:
    *   Set the `LLM_PROVIDER` environment variable to your desired provider (e.g., `export LLM_PROVIDER=openai`). If not set, it defaults to "ollama".
    *   Optionally, set `LLM_MODEL` to specify a model for the chosen provider (e.g., `export LLM_MODEL=gpt-4-turbo-preview`).
    *   Ensure relevant API keys (e.g., `OPENAI_API_KEY`) or AWS configurations are set in your environment if using cloud providers.

2.  **Navigate to the agent's directory**:
    ```bash
    cd path/to/your/llm_enhanced_agent
    ```

3.  **Run the `main.py` script**:
    ```bash
    python main.py
    ```
    Or, if you have multiple Python versions:
    ```bash
    python3 main.py
    ```

3.  **Interact with the Agent via CLI**:
    The CLI will start, and you'll see a prompt like `You: `. Type your message and press Enter. The agent will respond, showing its simulated LLM-enhanced output.
    ```
    LLM-Enhanced Agent CLI
    ------------------------------
    Type 'exit' or 'quit' to stop.
    You: Hello there!
    Agent: Agent: Here's what the LLM (Ollama/mistral) came up with: Hello! It's nice to meet you. How can I help you today?
    You: exit
    Exiting agent CLI. Goodbye!
    ```
    *(The exact LLM response will vary.)*

### Web UI (Streamlit)

This agent also comes with a simple web-based user interface built with Streamlit.

1.  **Install Streamlit (if not already installed)**:
    Refer to the "Prerequisites" section above if you also need to install `ollama`. Streamlit can be installed via pip:
    ```bash
    pip install streamlit
    ```
    *(Ensure your environment has the `ollama` package installed and Ollama service is running with the required model pulled, as per Prerequisites.)*

2.  **Run the Streamlit App**:
    To run the web UI, navigate to the root directory of this repository (where the main `README.md` is) and use the following command in your terminal:
    ```bash
    streamlit run llm_enhanced_agent/app_ui.py
    ```
    This will typically open the application in your default web browser.

3.  **Interact with the Agent via Web**:
    *   The web page will display a title and a text input box.
    *   Type your query into the text box.
    *   Click the "Send to Agent" button.
    *   The agent's response will appear below the button.
