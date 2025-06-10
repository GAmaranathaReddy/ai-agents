# Environment-Controlled Agent

## Environment-Controlled Agent (LLM-Powered Decision Making)

An Environment-Controlled Agent operates within a defined environment by following a perception-action loop. This enhanced version uses a Large Language Model (LLM) via Ollama for its **Decision-Making** process, allowing it to pursue natural language goals.

The core cycle is:
1.  **Perception**: The agent observes the current state of its environment.
2.  **Decision-Making (LLM-driven)**: Based on a user-defined **natural language goal** and the perceived state, the agent uses an LLM to:
    *   Analyze the situation.
    *   Choose the best action from a predefined set (e.g., "toggle_light", "set_temperature VALUE", "do_nothing").
    *   Determine any necessary value for that action (e.g., the target temperature).
    *   Provide an explanation for its choice.
    The LLM is instructed to return this decision in a structured JSON format.
3.  **Action**: The agent executes the LLM-chosen action, which modifies the environment's state.

This approach makes the agent more flexible, as its behavior can be dynamically altered by changing its natural language goal, without reprogramming its core decision logic (which is now offloaded to the LLM).

## Implementation

This project demonstrates the LLM-enhanced Environment-Controlled Agent:

1.  **`environment.py` (`Environment` class)**:
    *   Manages the environment's state (e.g., `light_on`, `temperature`).
    *   Provides `get_state()` and `apply_action(action, value)` methods. This remains unchanged from the previous version.

2.  **`agent.py` (`EnvironmentControlledAgent` class - Updated)**:
    *   Initialized with an `Environment` instance and an Ollama `llm_model` name (e.g., "mistral").
    *   Stores a `current_goal` as a natural language string (e.g., "Keep the room well-lit and cool."). Includes a default goal.
    *   **`set_goal(natural_language_goal: str)` method**: Allows users to update the agent's `current_goal`.
    *   **`decide_action(current_state: dict)` method (Rewritten)**:
        *   Constructs a detailed prompt for the configured Ollama LLM. This prompt includes:
            *   The agent's `current_goal`.
            *   The `current_state` of the environment (as a JSON string).
            *   A list of `available_actions` with descriptions of their effects and expected arguments.
        *   Instructs the LLM to choose the best action and any necessary `action_value` to progress towards the goal, and to provide an `explanation`. The LLM is asked to return this in JSON format: `{"action_name": "chosen_action", "action_value": value_if_any, "explanation": "reason_for_action"}`.
        *   Calls `ollama.chat()` with `format='json'`.
        *   Parses the JSON response from the LLM.
        *   Includes validation for the `action_name` and `action_value` returned by the LLM.
        *   Returns the `action_name`, `action_value`, and the LLM's `explanation`.
        *   Includes error handling for LLM communication and JSON parsing, defaulting to "do_nothing".
    *   `perceive()` and `execute_action()` methods remain largely the same.

3.  **`main.py` (CLI - Updated)**:
    *   The CLI simulation loop now accommodates the three return values from `decide_action` (action, value, explanation) and prints the LLM's explanation for each step.
    *   Includes a simple mechanism to externally modify the environment state during the simulation to make it more dynamic.

4.  **`app_ui.py` (Streamlit UI - Updated)**:
    *   The Streamlit UI now features a text input field in the sidebar allowing users to set or update the agent's `current_goal` in natural language.
    *   The simulation log in the UI displays the active goal for each step and the LLM's `explanation` for the action taken, providing transparency into the agent's reasoning.

## Prerequisites & Setup

1.  **Ollama and LLM Model**:
    *   **Install Ollama**: Ensure Ollama is installed and running. See the [Ollama official website](https://ollama.com/).
    *   **Pull an LLM Model**: The agent defaults to `"mistral"`. You need this model (or your chosen alternative that's good at following instructions and generating JSON) pulled in Ollama.
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
