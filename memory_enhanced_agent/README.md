# Memory-Enhanced Agent

## Memory-Enhanced Agent (LLM-Powered)

A Memory-Enhanced Agent maintains and utilizes a memory of past interactions and learned facts to inform its current and future behavior. This version is **LLM-powered**, using Ollama to:
1.  Understand user input in a conversational context.
2.  Extract new facts explicitly stated by the user.
3.  Generate responses that are aware of both learned facts and recent conversation history.

The core components are:
*   **Memory Store (`memory.py`)**: Stores key-value facts and a chronological log of user-agent interactions.
*   **LLM-Driven Agent Logic (`agent.py`)**: Orchestrates interaction with the user and the memory, using an LLM for NLU, fact extraction, and response generation.

## Implementation

This project demonstrates the LLM-powered Memory-Enhanced Agent:

1.  **`memory.py` (`Memory` class)**:
    *   Remains largely the same, providing methods to `add_fact` (which updates if key exists), `get_fact`, `get_all_facts`, `log_interaction`, and `get_conversation_history`.

2.  **`agent.py` (`MemoryEnhancedAgent` class - Updated)**:
    *   Initialized with an Ollama model name (e.g., "mistral").
    *   The old regex-based `_extract_facts` and rule-based `_generate_response` methods are removed.
    *   The main `chat(user_input: str)` method is rewritten:
        *   It retrieves all known facts and the last N turns of conversation history from the `Memory` instance.
        *   It constructs a detailed prompt for the configured Ollama LLM. This prompt includes:
            *   The current `user_input`.
            *   The `known_facts` (as a JSON string).
            *   The `recent_conversation_history` (formatted as dialogue).
            *   Instructions for the LLM to:
                1.  Generate a natural, conversational `response` to the user, using known facts and history for context.
                2.  Identify any `new_facts_to_store` (as a dictionary) explicitly stated by the user in their *current* message.
                3.  Return this output as a single JSON object: `{"response": "...", "new_facts_to_store": {"key": "value", ...}}`.
        *   It calls `ollama.chat()` with `format='json'` to get the structured response.
        *   It parses the JSON to extract the `agent_reply` and any `new_facts`.
        *   If `new_facts` are present and valid, they are added to the agent's memory using `self.memory.add_fact()`.
        *   It includes error handling for LLM communication and JSON parsing.
        *   The `user_input` and the final `agent_reply` are logged to the conversation history in memory.

3.  **`main.py` (CLI)** and **`app_ui.py` (Streamlit UI)**:
    *   These interfaces interact with the LLM-enhanced agent.
    *   The Streamlit UI (`app_ui.py`) allows users to chat with the agent and inspect its learned facts and internal conversation log, now reflecting the LLM's influence on memory and responses.

This architecture allows the agent to have more natural conversations, learn facts more flexibly from user statements, and use its memory more intelligently, all mediated by the LLM.

## Prerequisites & Setup

1.  **Ollama and LLM Model**:
    *   **Install Ollama**: Ensure Ollama is installed and running. See the [Ollama official website](https://ollama.com/).
    *   **Pull an LLM Model**: The agent defaults to `"mistral"`. You need this model (or your chosen alternative that's good at conversational tasks and following JSON format instructions) pulled in Ollama.
      ```bash
      ollama pull mistral
      ```
    *   **Install Ollama Python Client**:
      ```bash
      pip install ollama
      ```

2.  **Streamlit (for UI)**:
    *   If you want to use the web UI, install Streamlit:
      ```bash
      pip install streamlit
      ```

*(If using Poetry for the main project, add `ollama` and `streamlit` to your `pyproject.toml` and run `poetry install`.)*

## How to Run

**(Ensure you have completed all Prerequisites & Setup steps above: Ollama running, model pulled, and Python packages installed.)**

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
