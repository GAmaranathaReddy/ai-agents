# Tool-Enhanced Agent

## Tool-Enhanced Agent Pattern

A Tool-Enhanced Agent is an autonomous or semi-autonomous system that can leverage external tools or functions to extend its capabilities beyond its core programming. Instead of having all functionalities built-in, the agent possesses a mechanism to identify when a specific task can be better handled by a specialized tool, how to call that tool with the correct inputs, and how to integrate the tool's output back into its response or workflow.

The core components of this pattern typically include:
1.  **A set of available tools**: These are functions or services that perform specific tasks (e.g., fetching data, performing calculations, interacting with other systems).
2.  **Decision Logic (Router/Dispatcher)**: The agent needs to analyze incoming requests or its current goal to determine:
    *   If a tool is needed.
    *   Which specific tool is appropriate for the task.
    *   What arguments the tool requires.
3.  **Argument Parsing**: If a tool requires inputs, the agent must extract or derive these arguments from the user's request or its internal state.
4.  **Tool Execution**: The agent calls the selected tool with the prepared arguments.
5.  **Response Integration**: The agent takes the output from the tool and uses it to formulate a final response or to inform its next actions.

This pattern allows agents to be more versatile and powerful, as they can dynamically access specialized functionalities without needing to implement everything themselves.

## Implementation

This project provides a demonstration of the Tool-Enhanced Agent pattern:

1.  **`tools.py`**:
    *   Defines a set of simple Python functions that act as our tools:
        *   `get_current_datetime()`: Returns the current date and time.
        *   `calculate_sum(a: float, b: float)`: Returns the sum of two numbers.
        *   `get_weather(city: str)`: Returns a dummy weather string for a given city (simulating an API call).
    *   These functions are self-contained and perform specific, distinct tasks.

2.  **`agent.py`**:
    *   Defines the `ToolEnhancedAgent` class.
    *   The core logic resides in the `process_request(user_input: str)` method:
        *   **Decision Logic & Argument Parsing**:
            *   It converts the `user_input` to lowercase for case-insensitive matching.
            *   It uses `if/elif` conditions and regular expressions (`re.search`) to detect keywords and patterns associated with each tool:
                *   Keywords like "time", "date" trigger `get_current_datetime`. No arguments needed.
                *   Patterns like "sum of X and Y" or "add X plus Y" trigger `calculate_sum`. The regex captures the two numbers (`X` and `Y`) as arguments. These are then converted to floats.
                *   Patterns like "weather in [city]" or "what's the weather for [city]" trigger `get_weather`. The regex captures the `[city]` name as an argument.
        *   **Tool Execution**: If a pattern is matched and necessary arguments are successfully parsed:
            *   The corresponding function from `tools.py` is called.
        *   **Response Generation**:
            *   The output from the tool is used to construct a meaningful response to the user.
            *   If no tool-specific keywords/patterns are matched, the agent provides a default introductory response, listing its capabilities.
            *   Basic error handling is included if argument parsing fails (e.g., non-numeric input for sum).

3.  **`main.py`**:
    *   Provides a simple command-line interface (CLI) to interact with the `ToolEnhancedAgent`.
    *   It takes user input, passes it to the agent's `process_request` method, and prints the agent's response, which may be generated directly by the agent or be based on a tool's output.

This implementation clearly shows the agent's ability to understand different types of requests, select an appropriate tool, extract necessary information for that tool, execute it, and then present the result to the user.

## How to Run

1.  **Navigate to the project directory**:
    Open your terminal or command prompt.
    ```bash
    cd path/to/your/tool_enhanced_agent
    ```

2.  **Ensure all files are present**:
    You should have `agent.py`, `tools.py`, and `main.py` in this directory.

3.  **Run the `main.py` script**:
    ```bash
    python main.py
    ```
    Or, if you have multiple Python versions, you might need to use `python3`:
    ```bash
    python3 main.py
    ```

4.  **Interact with the Agent**:
    The CLI will start. You can then type your requests.

    **Example Commands**:
    *   `What time is it?`
    *   `Could you tell me the current date?`
    *   `Calculate the sum of 10 and 5`
    *   `add 7.5 plus 2.5`
    *   `What's the weather in London?`
    *   `weather for Paris`
    *   `Tell me the weather in Berlin`
    *   `Hello` (to get the default response)

    **Example Interaction**:
    ```
    Tool-Enhanced Agent CLI
    Powered by: ToolBot Alpha
    You can ask for the current time/date, calculate sums (e.g., 'add 10 and 5'),
    or get the weather (e.g., 'what's the weather in London?').
    Type 'exit' or 'quit' to stop.
    ------------------------------
    You: What is the current time?
    Agent: The current date and time is: YYYY-MM-DD HH:MM:SS
    You: add 15 and 30
    Agent: The sum of 15 and 30 is 45.0.
    You: What's the weather in Tokyo?
    Agent: The weather in Tokyo is experiencing light showers.
    You: exit
    Exiting agent CLI. Goodbye!
    ```
    *(Note: The exact date/time will reflect when you run it)*
