# LLM-Enhanced Agent

## LLM-Enhanced Agent Pattern

The LLM-Enhanced Agent pattern involves integrating a Large Language Model (LLM) into an agent's decision-making or response-generation process. Instead of relying solely on pre-programmed logic or rules, the agent leverages the LLM's capabilities (e.g., natural language understanding, generation, reasoning) to handle more complex tasks, understand nuanced user inputs, or provide more human-like and contextually aware responses.

The core idea is to use the LLM as a "cognitive core" or a specialized component that the main agent system can query. The agent prepares the input for the LLM, calls the LLM, and then processes the LLM's output to fit the overall task or conversation.

This pattern allows developers to build more sophisticated and flexible agents by combining the strengths of traditional software engineering with the power of modern LLMs.

## Implementation

This project provides a very simple demonstration of this pattern:

1.  **`agent.py`**:
    *   Defines an `LLMEnhancedAgent` class.
    *   The `__init__` method initializes the agent and allows specifying a conceptual name for the LLM service it might interact with.
    *   The `get_llm_response(user_input)` method *simulates* an interaction with an LLM. In a real-world application, this method would contain the actual API call to an LLM service (like OpenAI's API, Google's PaLM API, or a self-hosted model). For this example, it simply prepends a string to the user's input to mimic an LLM's contribution.
    *   The `process_request(user_input)` method orchestrates the interaction: it takes user input, calls `get_llm_response` to get the LLM's (simulated) output, and then could (though in this simple example doesn't extensively) add further agent-specific processing before returning the final response.

2.  **`main.py`**:
    *   Provides a simple command-line interface (CLI) to interact with the `LLMEnhancedAgent`.
    *   It instantiates the agent and then enters a loop, taking user input, passing it to the agent's `process_request` method, and printing the agent's response.

The "enhancement" by the LLM is shown by how the `agent.py` takes the user's input, sends it to a (simulated) LLM, and incorporates the LLM's output into its final reply.

## How to Run

1.  **Navigate to the project directory**:
    Open your terminal or command prompt.
    ```bash
    cd path/to/your/llm_enhanced_agent
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
    The CLI will start, and you'll see a prompt like `You: `. Type your message and press Enter. The agent will respond, showing its simulated LLM-enhanced output.
    ```
    LLM-Enhanced Agent CLI
    ------------------------------
    Type 'exit' or 'quit' to stop.
    You: Hello there!
    Agent: Agent: Here's what the LLM (MyCustomLLM) came up with: [MyCustomLLM says]: You said 'Hello there!'. That's interesting!
    You: exit
    Exiting agent CLI. Goodbye!
    ```

### Web UI (Streamlit)

This agent also comes with a simple web-based user interface built with Streamlit.

1.  **Install Streamlit**:
    If you haven't already, you'll need to install Streamlit. If you are managing dependencies with Poetry for the main project, you might add it there. Otherwise, for a quick local install:
    ```bash
    pip install streamlit
    ```
    (If you are using Poetry and want to add it to this specific project's dev dependencies, you could navigate to the `llm_enhanced_agent` directory and run `poetry add streamlit --group dev` if it were a separate poetry project, or add it to the main project's `pyproject.toml`.)

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
