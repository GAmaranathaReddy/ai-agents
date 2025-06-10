# Fixed Automation Agent

## Fixed Automation Agent (LLM-Enhanced for NLU)

A Fixed Automation Agent typically operates based on a predefined set of rules or a fixed workflow. This enhanced version leverages a Large Language Model (LLM) via Ollama for Natural Language Understanding (NLU), allowing it to interpret more flexible user commands while still executing a fixed set of predefined tasks.

Instead of relying on rigid keyword matching or regex, the agent sends the user's natural language input to an LLM. The LLM's role is to:
1.  Identify which of the agent's known tasks the user intends to perform (e.g., "greet", "add", "multiply", "about").
2.  Extract necessary parameters for those tasks (e.g., numbers for addition/multiplication).
3.  Return this structured information (e.g., in JSON format) to the agent.

The agent then uses this structured output from the LLM to call its internal, fixed functions that perform the actual tasks. This combines the flexibility of natural language input with the reliability and predictability of fixed automation tasks.

## Implementation

This project demonstrates the LLM-enhanced Fixed Automation Agent pattern:

1.  **`automation.py` (`FixedAutomationAgent` class - Updated)**:
    *   The agent is initialized with an Ollama model name (e.g., "mistral").
    *   The core tasks (greeting, about, addition, multiplication) are implemented as private methods (`_perform_greeting()`, `_perform_about()`, `_perform_addition(num1, num2)`, `_perform_multiplication(num1, num2)`). These methods contain the actual fixed logic.
    *   The main `process_request(user_input: str)` method is rewritten:
        *   It constructs a detailed prompt for the configured Ollama LLM. This prompt instructs the LLM to analyze the `user_input`, identify the intended task from a predefined list ("greet", "about", "add", "multiply", "unknown"), and extract numbers if the task is "add" or "multiply".
        *   The LLM is specifically asked to respond in JSON format, e.g., `{"task": "add", "numbers": [5, 3]}`.
        *   It calls `ollama.chat()` with the user input and the prompt, requesting JSON output.
        *   It parses the JSON response from the LLM to get the identified `task` and `numbers`.
        *   Based on the `task`, it calls the appropriate private method (e.g., `_perform_addition(*numbers)`).
        *   It includes error handling for LLM communication issues and JSON parsing errors.
        *   It returns a dictionary containing the `user_input`, the `llm_interpretation` (parsed JSON), the `final_result` from the executed task, and any `error` messages.

2.  **`main.py` (CLI)**:
    *   Provides a command-line interface. It now prints the structured dictionary returned by `process_request`, showing both the LLM's interpretation and the final result.

3.  **`app_ui.py` (Streamlit UI - Updated)**:
    *   The Streamlit UI is updated to reflect the agent's new capabilities.
    *   It encourages natural language input.
    *   It displays the LLM's interpretation (the JSON) to provide transparency into how the user's command was understood, followed by the agent's final result or any errors.

The agent still performs a fixed set of tasks, but its ability to understand *how* to trigger those tasks is now enhanced by an LLM.

## Prerequisites & Setup

1.  **Ollama and LLM Model**:
    *   **Install Ollama**: Ensure Ollama is installed and running. See [Ollama official website](https://ollama.com/).
    *   **Pull an LLM Model**: The agent defaults to `"mistral"`. You need this model (or your chosen alternative that's good at following JSON format instructions) pulled in Ollama.
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
