# Environment-Controlled Agent

## Environment-Controlled Agent (LLM-Powered Decision Making via Abstraction Layer)

An Environment-Controlled Agent operates within a defined environment using a perception-action loop. This version uses a **centrally configured LLM provider** (via the common abstraction layer) for its **Decision-Making** process, allowing it to pursue natural language goals.

The core cycle:
1.  **Perception**: Agent observes the environment's current state.
2.  **Decision-Making (LLM-driven via Abstraction Layer)**: Based on a natural language `current_goal` and the perceived state, the agent uses the configured LLM provider to:
    *   Analyze the situation against the goal.
    *   Choose the best action from a predefined set (e.g., "toggle_light", "set_temperature VALUE", "do_nothing").
    *   Determine any necessary value for that action.
    *   Provide an `explanation` for its choice.
    The LLM is instructed (via a prompt) to return this decision in a structured JSON format.
3.  **Action**: Agent executes the LLM-chosen action, modifying the environment.

This makes the agent flexible, as its behavior adapts to different natural language goals without reprogramming, leveraging the chosen LLM backend.

## Implementation

1.  **`environment.py` (`Environment` class)**:
    *   Manages environment state (`light_on`, `temperature`). Unchanged.

2.  **`agent.py` (`EnvironmentControlledAgent` class - Updated)**:
    *   No longer directly manages LLM client details or model names.
    *   In `__init__`, it calls `get_llm_provider_instance()` from `common.llm_config` to get the globally configured LLM provider (Ollama, OpenAI, etc.).
    *   Stores a `current_goal` (natural language string with a default).
    *   `set_goal(natural_language_goal: str)`: Allows updating the agent's goal.
    *   `decide_action(current_state: dict)` (Rewritten):
        *   Constructs a prompt for the configured LLM provider, including the `current_goal`, `current_state` (as JSON), and available actions with descriptions.
        *   Instructs the LLM to return its decision (action, value, explanation) in JSON format.
        *   Calls `self.llm_provider.chat(..., request_json_output=True)` to get the LLM's structured decision.
        *   Parses the JSON and includes validation.
        *   Returns `action_name`, `action_value`, and `explanation`.
        *   Includes generalized error handling for LLM communication and JSON parsing.

3.  **`main.py` (CLI - Updated)**:
    *   Interacts with the refactored agent. Prints the LLM's explanation for each step. Includes external event simulation.

4.  **`app_ui.py` (Streamlit UI - Updated)**:
    *   Allows users to set/update the agent's `current_goal` via a sidebar text input.
    *   Displays the active goal and the LLM's `explanation` for each action in the simulation log.

## Prerequisites & Setup

1.  **LLM Provider Configuration**:
    *   This agent uses the centrally configured LLM provider. Ensure you have set up your desired LLM provider (Ollama, OpenAI, Gemini, or AWS Bedrock) and configured the necessary environment variables (e.g., `LLM_PROVIDER`, `OLLAMA_MODEL`, `OPENAI_API_KEY`, etc.).
    *   **Refer to the "Multi-LLM Provider Support" section in the main project README** for detailed instructions on setting up environment variables and installing provider-specific SDKs. A model good at instruction-following and generating JSON is recommended.

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
    cd path/to/your/environment_controlled_agent
    ```

2.  **Ensure all files are present**:
    You should have `agent.py`, `environment.py`, and `main.py` in this directory.

3.  **Run the `main.py` script**:
    ```bash
    python main.py
    ```
    Or using `python3`:
    ```bash
    python3 main.py
    ```

3.  **Observe the Simulation via CLI**:
    The script runs a simulation. For each step, it prints the perceived state, the agent's (LLM-driven) decided action and value, the LLM's reasoning, the execution result, and the new environment state.
    ```
    --- Step 1/8 ---
    Agent perceives state: {'light_on': False, 'temperature': 20}
    Agent decides to: toggle_light with value None
    Agent's reasoning: "The light is currently off, and the goal is to maintain a well-lit environment, so turning on the light is the first priority."
    Action execution result: Light turned on.
    New environment state: {'light_on': True, 'temperature': 20}
    (Pausing for 2s...)
    ```
    *(Exact LLM explanations and decisions might vary.)*

### Web UI (Streamlit)

The LLM-powered Environment-Controlled Agent's decision process is best observed via its Streamlit UI.

1.  **Ensure Dependencies are Installed**:
    Make sure `streamlit` and `ollama` are installed (see Prerequisites).

2.  **Run the Streamlit App**:
    Navigate to the root directory of this repository and execute:
    ```bash
    streamlit run environment_controlled_agent/app_ui.py
    ```
    This will open the UI in your web browser.

3.  **Interact with the Simulation via Web**:
    *   The UI displays the current environment state.
    *   In the sidebar, you can view and **update the agent's current goal** using natural language (e.g., "Make the room dark and warm, around 28 degrees Celsius", "Prioritize energy saving: turn off light if not needed and keep temperature moderate at 20 degrees").
    *   Click "Run Next Step" to advance the simulation.
    *   The "Simulation Log" shows each step's details: the goal active during that step, perceived state, decided action and value, the **LLM's reasoning** for the action, the execution result, and the new environment state.
    *   Use the "Reset Simulation" button to start over with the default goal.
```
