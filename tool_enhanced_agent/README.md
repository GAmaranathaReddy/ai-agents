# Tool-Enhanced Agent

## Tool-Enhanced Agent (LLM-Powered NLU)

A Tool-Enhanced Agent leverages external tools or functions to extend its capabilities. This version is enhanced with a Large Language Model (LLM) via Ollama for Natural Language Understanding (NLU), enabling it to interpret user requests in natural language to select the appropriate tool and extract its arguments.

The core components of this enhanced pattern include:
1.  **A set of available tools**: Functions performing specific tasks (e.g., `get_current_datetime`, `calculate_sum`, `get_weather`).
2.  **LLM-Powered NLU**: The agent uses an LLM to:
    *   Analyze the user's natural language input.
    *   Identify which of the available tools is best suited for the request.
    *   Extract the necessary arguments for the chosen tool from the input.
    *   Return this information in a structured format (e.g., JSON).
3.  **Tool Execution**: The agent calls the selected tool function with the LLM-extracted arguments.
4.  **Response Generation**: The agent formulates a final response based on the tool's output.

This approach allows for more flexible and intuitive interaction with tool-using agents, as users are not restricted to rigid command formats.

## Implementation

This project demonstrates the LLM-enhanced Tool-Enhanced Agent pattern:

1.  **`tools.py`**:
    *   Defines the actual Python functions that act as tools: `get_current_datetime()`, `calculate_sum(a, b)`, `get_weather(city)`. These remain simple and focused.

2.  **`agent.py` (`ToolEnhancedAgent` class - Updated)**:
    *   Initialized with an Ollama model name (e.g., "mistral").
    *   Maintains a `tools_description` dictionary detailing each available tool and its expected arguments. This information is used to construct a prompt for the LLM.
    *   Keeps a `callable_tools` dictionary mapping tool names (strings) to the actual tool functions.
    *   The `process_request(user_input: str)` method is rewritten:
        *   It builds a detailed prompt for the LLM, including the descriptions of available tools and the user's input. It instructs the LLM to identify the most appropriate tool and extract its arguments, responding in JSON format (e.g., `{"tool_name": "calculate_sum", "arguments": {"a": 10, "b": 5}}`).
        *   It calls `ollama.chat()` with `format='json'` to get the LLM's interpretation.
        *   It parses the JSON response to get the `tool_name` and `arguments` dictionary.
        *   If a valid tool is identified in `callable_tools`:
            *   It calls the tool function, dynamically passing the extracted `arguments` using `**arguments`.
            *   It handles potential type errors for arguments (e.g., converting sum arguments to float).
        *   It includes error handling for LLM communication, JSON parsing, and tool execution issues.
        *   It returns a structured dictionary containing `user_input`, `llm_interpretation` (the parsed JSON from LLM), `tool_used`, `tool_input_params`, `tool_output_raw`, `final_response`, and any `error` messages.

3.  **`main.py` (CLI)**:
    *   The CLI now interacts with the LLM-enhanced agent, displaying the structured dictionary output, which includes the LLM's interpretation of the command.

4.  **`app_ui.py` (Streamlit UI - Updated)**:
    *   The Streamlit UI is updated to encourage natural language input.
    *   It now displays the "LLM Interpretation" (the JSON from Ollama showing tool choice and arguments) to provide transparency, alongside other details like the raw tool output and the agent's final response.

## Prerequisites & Setup

1.  **Ollama and LLM Model**:
    *   **Install Ollama**: Ensure Ollama is installed and running. See [Ollama official website](https://ollama.com/).
    *   **Pull an LLM Model**: The agent defaults to `"mistral"`. You need this model (or your chosen alternative that's good at following JSON format instructions and tool descriptions) pulled in Ollama.
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
