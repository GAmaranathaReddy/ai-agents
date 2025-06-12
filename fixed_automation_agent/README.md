# Fixed Automation Agent

## Fixed Automation Agent (LLM-Enhanced NLU via Abstraction Layer)

A Fixed Automation Agent typically operates based on a predefined set of rules or a fixed workflow. This enhanced version leverages a **centrally configured LLM provider** (via the common abstraction layer) for Natural Language Understanding (NLU). This allows the agent to interpret more flexible user commands while still executing a fixed set of predefined tasks.

The agent sends the user's natural language input to the configured LLM provider. The LLM's role, guided by a specific prompt, is to:
1.  Identify which of the agent's known tasks the user intends to perform (e.g., "greet", "add", "multiply", "about").
2.  Extract necessary parameters for those tasks (e.g., numbers for addition/multiplication).
3.  Return this structured information (e.g., in JSON format) to the agent.

The agent then uses this structured output from the LLM to call its internal, fixed functions that perform the actual tasks.

## Implementation

This project demonstrates the LLM-enhanced Fixed Automation Agent pattern using the common LLM provider abstraction:

1.  **`automation.py` (`FixedAutomationAgent` class - Updated)**:
    *   The agent no longer directly manages LLM client (e.g., `ollama`) or model names.
    *   In its `__init__` method, it calls `get_llm_provider_instance()` from `common.llm_config` to obtain a ready-to-use LLM provider object (which could be Ollama, OpenAI, Gemini, or Bedrock, based on environment variables).
    *   The core tasks (greeting, about, addition, multiplication) remain as private methods (`_perform_greeting()`, etc.).
    *   The main `process_request(user_input: str)` method:
        *   Constructs a detailed prompt for the configured LLM provider. This prompt instructs the LLM to analyze the `user_input`, identify the intended task, and extract numbers if applicable, responding in JSON format.
        *   It calls `self.llm_provider.chat(..., request_json_output=True)` to get the LLM's interpretation.
        *   It parses the JSON response from the LLM to get the identified `task` and `numbers`.
        *   Based on the `task`, it calls the appropriate private method.
        *   Error handling for LLM communication and JSON parsing is generalized.
        *   It returns a dictionary containing `user_input`, `llm_interpretation` (parsed JSON), `final_result`, and any `error` messages.

2.  **`main.py` (CLI)**:
    *   Interacts with the refactored agent. It prints the structured dictionary from `process_request`, showing the LLM's interpretation and the final result.

3.  **`app_ui.py` (Streamlit UI - Updated)**:
    *   The Streamlit UI encourages natural language input.
    *   It displays the LLM's interpretation (the JSON from the provider) for transparency, followed by the agent's final result or any errors.

The agent still performs a fixed set of tasks, but its command understanding is now powered by the configured LLM provider through the abstraction layer.

## Prerequisites & Setup

1.  **LLM Provider Configuration**:
    *   This agent uses the centrally configured LLM provider. Ensure you have set up your desired LLM provider (Ollama, OpenAI, Gemini, or AWS Bedrock) and configured the necessary environment variables (e.g., `LLM_PROVIDER`, `OLLAMA_MODEL`, `OPENAI_API_KEY`, etc.).
    *   **Refer to the "Multi-LLM Provider Support" section in the main project README** for detailed instructions on setting up environment variables and installing provider-specific SDKs (like `ollama`, `openai`, `google-generativeai`, `boto3`).

2.  **Streamlit (for UI)**:
    *   If you want to use the web UI, install Streamlit (listed in this agent's `requirements.txt`):
      ```bash
      pip install streamlit
      ```

*(If using Poetry for the main project, ensure `streamlit` and the chosen LLM provider's SDK are added to your `pyproject.toml`.)*

## How to Run

**(Ensure you have completed all Prerequisites & Setup steps above: chosen LLM provider configured, its service running if needed, and Python packages installed.)**

### 1. Command-Line Interface (CLI)

1.  **Navigate to the agent's directory**:
    ```bash
    cd path/to/your/fixed_automation_agent
    ```

2.  **Run the `main.py` script**:
    ```bash
    python main.py
    ```
    Or using `python3`:
    ```bash
    python3 main.py
    ```

3.  **Interact with the Agent via CLI**:
    The CLI will start. Type your commands in natural language.
    ```
    User: hello there
      LLM Interpretation: {'task': 'greet', 'numbers': None}
      Agent Final Result: Hello! I am RuleBot V2 (LLM-Enhanced). I can help with greetings, info about myself, addition, and multiplication.

    User: what is 12 plus 8
      LLM Interpretation: {'task': 'add', 'numbers': [12, 8]}
      Agent Final Result: The sum of 12 and 8 is 20.0.
    ```

### Web UI (Streamlit)

This agent also features an LLM-enhanced web UI built using Streamlit.

1.  **Ensure Dependencies are Installed**:
    Make sure `streamlit` and `ollama` are installed (see Prerequisites).

2.  **Run the Streamlit App**:
    Navigate to the root directory of this repository and execute:
    ```bash
    streamlit run fixed_automation_agent/app_ui.py
    ```
    This will open the UI in your web browser.

3.  **Interact with the Agent via Web**:
    *   The web page will provide an input field for your command.
    *   Enter commands in natural language (e.g., "Can you tell me what 5 times 7 is?", "Say hi to me", "What are you?").
    *   Click "Send Command".
    *   The UI will display the "LLM Interpretation" (the JSON object showing how the LLM understood your command) and then the "Agent's Final Result".
```
