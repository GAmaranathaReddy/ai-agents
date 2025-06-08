# Memory-Enhanced Agent

## Memory-Enhanced Agent Pattern

A Memory-Enhanced Agent is an agent that maintains and utilizes a memory of past interactions, learned facts, or contextual information to inform its current and future behavior. This allows the agent to provide more personalized, coherent, and context-aware responses over time.

The core components of this pattern include:

1.  **Memory Store**: A mechanism for storing information. This can be short-term (e.g., current conversation context) or long-term (e.g., user preferences, facts learned across multiple sessions).
    *   **Fact Memory**: Stores specific pieces of information (e.g., "user's name is Alice," "user's favorite color is blue").
    *   **Conversation History**: Keeps a log of the dialogue turns between the user and the agent.

2.  **Memory Operations**:
    *   **Writing/Encoding**: Processes new information from interactions and stores it appropriately in the memory. This might involve parsing input to extract relevant facts.
    *   **Reading/Retrieval**: Accesses stored information to make decisions or formulate responses. This could involve querying for specific facts or reviewing recent conversation history.

3.  **Agent Logic**: The agent's core processing is modified to interact with its memory.
    *   Before responding, it might retrieve relevant information.
    *   It might explicitly acknowledge learned information.
    *   It logs interactions to build up its history.

This pattern enables agents to move beyond stateless, purely reactive responses and engage in more meaningful, continuous dialogues.

## Implementation

This project demonstrates a simplified Memory-Enhanced Agent:

1.  **`memory.py`**:
    *   Defines a `Memory` class.
    *   Internally, it uses:
        *   A dictionary (`_facts`) to store key-value pieces of information (e.g., `{"name": "Alice"}`).
        *   A list (`_conversation_history`) to store tuples of (user_input, agent_response).
    *   Provides methods:
        *   `add_fact(key, value)`: To store or update a fact (keys are stored case-insensitively).
        *   `get_fact(key)`: To retrieve a fact.
        *   `log_interaction(user_input, agent_response)`: To add a turn to the history.
        *   `get_conversation_history()`: To retrieve the full dialogue log.
        *   `get_all_facts()`: To retrieve all learned facts.
        *   `clear_facts()`, `clear_history()`: For managing memory content.

2.  **`agent.py`**:
    *   Defines the `MemoryEnhancedAgent` class, which contains an instance of the `Memory` class.
    *   Its `chat(user_input: str)` method is the core of its processing:
        *   **Fact Extraction**: The private `_extract_facts(user_input)` method uses simple regular expressions to identify and extract potential facts from the user's input (e.g., "My name is John" -> `{"name": "John"}`; "I like blue" -> `{"favorite_color": "blue"}`; "I live in Paris" -> `{"location": "Paris"}`).
        *   **Memory Update**: If new or updated facts are extracted, they are added to the agent's `memory` instance.
        *   **Contextual Response Generation**: The private `_generate_response(user_input, extracted_facts)` method formulates the agent's reply.
            *   It checks if the user is asking a direct question about a stored fact (e.g., "What is my name?"). If so, it retrieves the fact from memory and uses it in the answer.
            *   It acknowledges newly learned information (e.g., "Nice to meet you, John!").
            *   It uses stored facts, like the user's name, to personalize greetings if available.
        *   **History Logging**: After generating a response, the `user_input` and `agent_response` are logged to the `memory`'s conversation history.

3.  **`main.py`**:
    *   Provides a simple command-line interface (CLI) for a conversational interaction.
    *   Users can chat with the agent over multiple turns.
    *   A special command `showmemory` allows the user to inspect the current state of the agent's facts and conversation history during the session.
    *   The agent demonstrates its ability to recall and use information (like the user's name or favorite color) from previous turns in the ongoing conversation.

This setup illustrates how an agent can learn from interactions, store that learning, and then use it to provide more relevant and personalized responses in subsequent turns.

## How to Run

1.  **Navigate to the project directory**:
    Open your terminal or command prompt.
    ```bash
    cd path/to/your/memory_enhanced_agent
    ```

2.  **Ensure all files are present**:
    You should have `agent.py`, `memory.py`, and `main.py` in this directory.

3.  **Run the `main.py` script**:
    ```bash
    python main.py
    ```
    Or, if you have multiple Python versions, you might need to use `python3`:
    ```bash
    python3 main.py
    ```

4.  **Interact with the Agent**:
    The CLI will start. You can then chat with the agent.

    **Example Conversation**:
    ```
    Memory-Enhanced Agent CLI - Chat with RecallBot
    The agent can remember your name, favorite color, and other details you share.
    Try saying: 'My name is [Your Name]', 'I like [color]', 'My favorite food is [food]'.
    Then ask: 'What is my name?', 'What is my favorite color?'.
    Type 'exit', 'quit', or 'bye' to end the chat.
    Type 'showmemory' to see what the agent remembers (facts and history).
    ------------------------------
    You: Hello there
    Agent: Hello! How can I help you today?
    You: My name is Alice.
    Agent: Nice to meet you, Alice! How can I help you today?
    You: I like the color red
    Agent: Noted, Alice! Your favorite color is red.
    You: I live in Wonderland
    Agent: Okay, Alice, I'll remember you live in Wonderland.
    You: What is my name?
    Agent: Alice, your name is Alice.
    You: What is my favorite color?
    Agent: Alice, your favorite color is red.
    You: Where do I live?
    Agent: Alice, you live in Wonderland.
    You: showmemory

    --- Agent's Current Memory ---
    Facts: {'name': 'Alice', 'favorite_color': 'red', 'location': 'Wonderland'}
    History:
      user: Hello there
      agent: Hello! How can I help you today?
      user: My name is Alice.
      agent: Nice to meet you, Alice! How can I help you today?
      user: I like the color red
      agent: Noted, Alice! Your favorite color is red.
      user: I live in Wonderland
      agent: Okay, Alice, I'll remember you live in Wonderland.
      user: What is my name?
      agent: Alice, your name is Alice.
      user: What is my favorite color?
      agent: Alice, your favorite color is red.
      user: Where do I live?
      agent: Alice, you live in Wonderland.
    ------------------------------

    You: exit
    Agent: Goodbye, Alice!
    ```

### Web UI (Streamlit)

The Memory-Enhanced Agent also features an interactive chat interface built with Streamlit. This UI allows you to converse with the agent and inspect its memory.

1.  **Install Streamlit**:
    If you haven't already, you'll need to install Streamlit. If your main project uses Poetry, consider adding Streamlit as a dependency there. For a standard local installation:
    ```bash
    pip install streamlit
    ```

2.  **Run the Streamlit App**:
    To launch the web UI, open your terminal, navigate to the root directory of this repository (where the main `README.md` is), and execute the command:
    ```bash
    streamlit run memory_enhanced_agent/app_ui.py
    ```
    This will typically open the application in your default web browser.

3.  **Interact with the Agent via Web**:
    *   The main part of the page is a chat interface. Enter your messages in the input box at the bottom.
    *   The conversation will be displayed above the input box.
    *   The sidebar provides options to view the agent's memory:
        *   **"Learned Facts"**: Shows key-value pairs the agent has learned (e.g., your name, favorite color).
        *   **"Agent's Internal Conversation Log"**: Displays the history of interactions as recorded by the agent itself.
        *   A "Refresh Memory View" button in the sidebar can be used to update these views after new interactions.
    *   Try having a conversation where you tell the agent your name or preferences, and then ask it about them later to see its memory in action.
