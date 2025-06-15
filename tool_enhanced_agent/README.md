# Tool-Enhanced Agent

## Tool-Enhanced Agent (LLM-Powered NLU via Abstraction Layer)

A Tool-Enhanced Agent leverages external tools or functions to extend its capabilities. This version is enhanced with a **centrally configured LLM provider** (via the common abstraction layer) for Natural Language Understanding (NLU). This enables the agent to interpret user requests in natural language to select the appropriate tool and extract its arguments.

The core components:
1.  **Available Tools**: Functions performing specific tasks (e.g., `get_current_datetime`, `calculate_sum`, `get_weather`).
2.  **LLM-Powered NLU (via Abstraction Layer)**: The agent uses the configured LLM provider to:
    *   Analyze the user's natural language input against a list of available tools and their descriptions.
    *   Identify the most suitable tool.
    *   Extract necessary arguments for that tool.
    *   Return this information in a structured JSON format.
3.  **Tool Execution**: The agent calls the selected tool function with the LLM-extracted arguments.
4.  **Response Generation**: The agent formulates a final response based on the tool's output.

This allows for flexible interaction, as users are not restricted to rigid command formats.

## Implementation

1.  **`tools.py`**:
    *   Defines the Python functions for tools: `get_current_datetime()`, `calculate_sum(a, b)`, `get_weather(city)`.

2.  **`agent.py` (`ToolEnhancedAgent` class - Updated)**:
    *   No longer directly manages LLM client details (e.g., `ollama`).
    *   In `__init__`, it calls `get_llm_provider_instance()` from `common.llm_config` to get a configured LLM provider (Ollama, OpenAI, Gemini, or Bedrock).
    *   Maintains `tools_description` (for LLM prompting) and `callable_tools` (mapping names to functions).
    *   The `process_request(user_input: str)` method:
        *   Builds a prompt for the LLM, including tool descriptions and user input, instructing it to identify the tool and extract arguments in JSON.
        *   Calls `self.llm_provider.chat(..., request_json_output=True)` to get the LLM's interpretation.
        *   Parses the JSON to get `tool_name` and `arguments`.
        *   Dynamically calls the chosen tool function with extracted arguments.
        *   Includes generalized error handling for LLM and tool execution.
        *   Returns a structured dictionary with `user_input`, `llm_interpretation`, `tool_used`, `tool_input_params`, `tool_output_raw`, `final_response`, and `error`.

3.  **`main.py` (CLI)**:
    *   Interacts with the refactored agent, displaying the structured output including LLM interpretation.

4.  **`app_ui.py` (Streamlit UI - Updated)**:
    *   Encourages natural language input.
    *   Displays the "LLM Interpretation" (JSON from the provider showing tool choice and args) for transparency, alongside other details.

## Prerequisites & Setup

1.  **LLM Provider Configuration**:
    *   This agent uses the centrally configured LLM provider. Ensure you have set up your desired LLM provider (Ollama, OpenAI, Gemini, or AWS Bedrock) and configured the necessary environment variables (e.g., `LLM_PROVIDER`, `OLLAMA_MODEL`, `OPENAI_API_KEY`, etc.).
    *   **Refer to the "Multi-LLM Provider Support" section in the main project README** for detailed instructions on setting up environment variables and installing provider-specific SDKs.

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
    cd path/to/your/tool_enhanced_agent
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
    The CLI will start. Type your requests in natural language.
    ```
    User Query: "What is the sum of 5 and 7?"
      LLM Interpretation: {'tool_name': 'calculate_sum', 'arguments': {'a': 5, 'b': 7}}
      Tool Used: calculate_sum
      Tool Input: {'a': 5, 'b': 7}
      Tool Raw Output: The sum of 5.0 and 7.0 is 12.0.
      Agent Final Response: The sum of 5.0 and 7.0 is 12.0.
    ------------------------------

    User Query: "show me the current time"
      LLM Interpretation: {'tool_name': 'get_current_datetime', 'arguments': {}}
      Tool Used: get_current_datetime
      Tool Input: None
      Tool Raw Output: 2023-10-27 10:30:00
      Agent Final Response: The current date and time is: 2023-10-27 10:30:00.
    ```
    *(Note: The exact date/time and LLM interpretation might vary slightly)*

### Web UI (Streamlit)

This Tool-Enhanced Agent also comes with an LLM-powered web UI built with Streamlit.

1.  **Ensure Dependencies are Installed**:
    Make sure `streamlit` and `ollama` are installed (see Prerequisites).

2.  **Run the Streamlit App**:
    Navigate to the root directory of this repository and execute:
    ```bash
    streamlit run tool_enhanced_agent/app_ui.py
    ```
    This will open the UI in your web browser.

3.  **Interact with the Agent via Web**:
    *   The web interface will encourage natural language input.
    *   A sidebar will list available tools and example natural language commands.
    *   Enter your query (e.g., "Can you tell me the weather in Paris?", "Add 100 to 55.5", "What's the date today?").
    *   Click "Send to Agent".
    *   The UI will display the "LLM Interpretation" (JSON showing tool and args), details of tool execution, and the agent's final response.
```
