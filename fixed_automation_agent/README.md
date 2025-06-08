# Fixed Automation Agent

## Fixed Automation Agent Pattern

A Fixed Automation Agent operates based on a predefined set of rules, logic, or a fixed workflow. Unlike more dynamic or intelligent agents, its behavior is explicitly programmed and does not typically involve learning or complex decision-making beyond its established rules.

These agents are designed for tasks that are well-defined and repetitive. They follow a script or a flowchart of operations. If the input matches a certain condition, a specific action is taken. If it doesn't match any predefined conditions, it usually responds with a default message or indicates an inability to process the input.

Examples include:
*   Simple chatbots with canned responses triggered by keywords.
*   Automated systems that perform specific data processing steps in a fixed order.
*   Basic calculators or tools that perform a limited set of operations based on direct commands.

The key characteristic is the deterministic nature of the agent's response to a given input.

## Implementation

This project provides a simple demonstration of the Fixed Automation Agent pattern:

1.  **`automation.py`**:
    *   Defines a `FixedAutomationAgent` class.
    *   The `__init__` method initializes the agent.
    *   The `process_request(user_input)` method contains the core logic. It uses a series of `if/elif/else` conditional statements (or in this case, direct `if` checks and a regex match) to determine the response:
        *   It checks for greeting keywords ("hello", "hi").
        *   It checks for an "about" command.
        *   It uses regular expressions (`re.match`) to parse commands for simple arithmetic:
            *   `add X Y`: to add two numbers.
            *   `multiply X Y`: to multiply two numbers.
        *   If none of these predefined rules are met, it returns a default "I don't understand" message.
    *   This demonstrates a rule-based approach where the agent's responses are directly tied to specific input patterns.

2.  **`main.py`**:
    *   Provides a simple command-line interface (CLI) to interact with the `FixedAutomationAgent`.
    *   It instantiates the agent, takes user input in a loop, passes it to the agent's `process_request` method, and prints the agent's fixed response.

The agent does not learn or adapt; it strictly follows its programmed rules. If you type "add 10 5", it will always give you the sum. If you type something outside its rules, like "what's the weather?", it will give its default non-understanding response.

## How to Run

1.  **Navigate to the project directory**:
    Open your terminal or command prompt.
    ```bash
    cd path/to/your/fixed_automation_agent
    ```

2.  **Run the `main.py` script**:
    ```bash
    python main.py
    ```
    Or, if you have multiple Python versions, you might need to use `python3`:
    ```bash
    python3 main.py
    ```

3.  **Interact with the Agent**:
    The CLI will start. Type your commands and press Enter.
    ```
    Fixed Automation Agent CLI
    Powered by: RuleBot V1
    Type 'exit' or 'quit' to stop.
    Example commands: 'hello', 'about', 'add X Y', 'multiply X Y'
    ------------------------------
    You: hello
    Agent: Hello! I am RuleBot V1. I can perform simple calculations like 'add X Y' or tell you about myself if you type 'about'.
    You: add 25 75
    Agent: The sum of 25 and 75 is 100.
    You: multiply 5 8
    Agent: The product of 5 and 8 is 40.
    You: tell me a joke
    Agent: I'm sorry, I don't understand that command. Try 'add X Y', 'multiply X Y', 'about', or say 'hello'.
    You: exit
    Exiting agent CLI. Goodbye!
    ```
