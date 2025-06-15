# Memory-Enhanced Agent

## Memory-Enhanced Agent (LLM-Powered via Abstraction Layer)

A Memory-Enhanced Agent maintains and utilizes a memory of past interactions and learned facts to inform its current behavior. This version is **LLM-powered**, using the **common LLM provider abstraction layer** (which can be Ollama, OpenAI, Gemini, or Bedrock based on global configuration) to:
1.  Understand user input in a conversational context.
2.  Extract new facts explicitly stated by the user.
3.  Generate responses that are aware of both learned facts and recent conversation history.

The core components:
*   **Memory Store (`memory.py`)**: Stores key-value facts and a chronological log of user-agent interactions.
*   **LLM-Driven Agent Logic (`agent.py`)**: Orchestrates interaction with the user and the memory, using the configured LLM provider for NLU, fact extraction, and response generation.

## Implementation

This project demonstrates the LLM-powered Memory-Enhanced Agent using the common LLM provider abstraction:

1.  **`memory.py` (`Memory` class)**:
    *   Provides methods to `add_fact` (updates if key exists), `get_fact`, `get_all_facts`, `log_interaction`, and `get_conversation_history`. Its functionality remains crucial.

2.  **`agent.py` (`MemoryEnhancedAgent` class - Updated)**:
    *   No longer directly manages LLM client details or model names.
    *   In `__init__`, it calls `get_llm_provider_instance()` from `common.llm_config` to get the globally configured LLM provider.
    *   The main `chat(user_input: str)` method:
        *   Retrieves known facts and recent conversation history from the `Memory` instance.
        *   Constructs a detailed prompt for the configured LLM provider. This prompt includes user input, known facts, history, and instructions for the LLM to generate a conversational `response` and identify `new_facts_to_store` (as a dictionary), returning both in a single JSON object.
        *   Calls `self.llm_provider.chat(..., request_json_output=True)` to get the structured response.
        *   Parses the JSON to extract the `agent_reply` and any `new_facts`.
        *   Adds valid `new_facts` to memory via `self.memory.add_fact()`.
        *   Includes generalized error handling for LLM communication and JSON parsing.
        *   Logs the user input and final agent reply.

3.  **`main.py` (CLI)** and **`app_ui.py` (Streamlit UI)**:
    *   Interact with the refactored agent. The UI continues to allow users to chat and inspect memory, which now reflects the LLM's influence.

This architecture allows for more natural conversations and flexible fact learning, mediated by the chosen LLM provider.

## Prerequisites & Setup

1.  **LLM Provider Configuration**:
    *   This agent uses the centrally configured LLM provider. Ensure you have set up your desired LLM provider (Ollama, OpenAI, Gemini, or AWS Bedrock) and configured the necessary environment variables (e.g., `LLM_PROVIDER`, `OLLAMA_MODEL`, `OPENAI_API_KEY`, etc.).
    *   **Refer to the "Multi-LLM Provider Support" section in the main project README** for detailed instructions on setting up environment variables and installing provider-specific SDKs. A model good at conversational tasks and following JSON format instructions is recommended.

2.  **Streamlit (for UI)**:
    *   Install Streamlit (listed in this agent's `requirements.txt`):
      ```bash
      pip install streamlit
      ```

*(If using Poetry for the main project, ensure `streamlit` and the chosen LLM provider's SDK are added to your `pyproject.toml`.)*

## How to Run

**(Ensure you have completed all Prerequisites & Setup steps above: chosen LLM provider configured, its service running if needed, and Python packages installed.)**

### 1. Command-Line Interface (CLI)

1.  **Navigate to the agent's directory**:
    ```bash
    cd path/to/your/memory_enhanced_agent
    ```

2.  **Ensure all files are present**:
    You should have `agent.py`, `memory.py`, and `main.py` in this directory.

3.  **Run the `main.py` script**:
    ```bash
    python main.py
    ```
    Or using `python3`:
    ```bash
    python3 main.py
    ```

3.  **Interact with the Agent via CLI**:
    The CLI will start. Chat with the agent naturally.
    ```
    Memory-Enhanced Agent CLI - Chat with RecallBot (LLM-Powered)
    The agent can remember your name, favorite color, and other details you share.
    Try saying: 'My name is [Your Name]', 'I like [color]', 'My favorite food is [food]'.
    Then ask: 'What is my name?', 'What is my favorite color?'.
    Type 'exit', 'quit', or 'bye' to end the chat.
    Type 'showmemory' to see what the agent remembers (facts and history).
    ------------------------------
    You: Hi, I'm Bob and I love the color green.
    Agent: Hi Bob! It's great to meet you. Green is a lovely color! I'll remember that. How can I help you today?
    You: What's my favorite color?
    Agent: Bob, if I remember correctly, your favorite color is green! Is there anything else I can help you with?
    You: showmemory

    --- Agent's Current Memory ---
    Facts: {'name': 'Bob', 'favorite_color': 'green'}
    History:
      user: Hi, I'm Bob and I love the color green.
      agent: Hi Bob! It's great to meet you. Green is a lovely color! I'll remember that. How can I help you today?
      user: What's my favorite color?
      agent: Bob, if I remember correctly, your favorite color is green! Is there anything else I can help you with?
    ------------------------------
    ```
    *(Exact LLM responses and extracted facts will vary based on the model and its interpretation.)*

### Web UI (Streamlit)

The Memory-Enhanced Agent's LLM-powered capabilities can be explored through its Streamlit UI.

1.  **Ensure Dependencies are Installed**:
    Make sure `streamlit` and `ollama` are installed (see Prerequisites).

2.  **Run the Streamlit App**:
    Navigate to the root directory of this repository and execute:
    ```bash
    streamlit run memory_enhanced_agent/app_ui.py
    ```
    This will open the UI in your web browser.

3.  **Interact with the Agent via Web**:
    *   Use the chat interface to converse with the agent.
    *   The sidebar allows you to inspect "Learned Facts" (extracted by the LLM) and the "Agent's Internal Conversation Log".
    *   Observe how the agent uses context from your conversation and previously learned facts in its responses, and how it identifies new facts.
```
