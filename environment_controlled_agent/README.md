# Environment-Controlled Agent

## Environment-Controlled Agent Pattern

An Environment-Controlled Agent, often a fundamental concept in AI and robotics, is an agent that operates within a defined environment by following a **perception-action loop**. The agent's behavior is determined by its interaction with this environment. The core cycle involves:

1.  **Perception**: The agent observes or senses the current state of its environment. This could involve reading sensor data, querying an API, or accessing shared state variables.
2.  **Decision-Making (or Deliberation)**: Based on the perceived state and its internal goals or programming, the agent decides what action to take (or to take no action). This logic can range from simple reflex rules to complex planning algorithms.
3.  **Action**: The agent executes the chosen action, which in turn can modify the state of the environment.

This loop repeats, allowing the agent to react to changes in the environment and work towards its objectives. The environment itself is a crucial component, as it defines the "world" the agent lives in, the states it can be in, and the actions that can affect it.

## Implementation

This project provides a simplified demonstration of the Environment-Controlled Agent pattern:

1.  **`environment.py`**:
    *   Defines an `Environment` class.
    *   This class manages a simple state consisting of two variables:
        *   `light_on` (boolean): Represents whether a light is on or off.
        *   `temperature` (integer): Represents the current temperature.
    *   It implements:
        *   `get_state()`: Returns the current dictionary of states.
        *   `apply_action(action: str, value: any = None)`: Modifies the environment's state based on predefined actions:
            *   `"toggle_light"`: Flips the boolean value of `light_on`.
            *   `"set_temperature"`: Sets the `temperature` to a given `value`.
            *   It returns a string describing the outcome of the action (e.g., "Light turned on.").

2.  **`agent.py`**:
    *   Defines the `EnvironmentControlledAgent` class.
    *   It takes an `Environment` instance during initialization, establishing the link between the agent and its world.
    *   It implements the core perception-action loop methods:
        *   `perceive()`: Calls its environment's `get_state()` method to get the current environmental conditions.
        *   `decide_action(current_state: dict)`: Contains simple rule-based logic to choose an action:
            *   If the `light_on` state is `False`, it decides to `"toggle_light"`.
            *   If the `temperature` is below 18, it decides to `"set_temperature"` to 22.
            *   If the `temperature` is above 25, it decides to `"set_temperature"` to 22.
            *   Otherwise, it decides to `"do_nothing"`.
        *   `execute_action(action: str, value: any = None)`: If the action is not `"do_nothing"`, it calls the `apply_action` method on its `environment` instance, passing the chosen action and any necessary value. It returns the result message from the environment.

3.  **`main.py`**:
    *   Sets up and runs a simulation of the agent interacting with the environment.
    *   It initializes an `Environment` instance and an `EnvironmentControlledAgent` instance (passing the environment to the agent).
    *   It then runs a loop for a fixed number of steps (e.g., 10 steps). In each step:
        1.  The agent perceives the environment's state, and the state is printed.
        2.  The agent decides on an action based on this state, and the intended action is printed.
        3.  The agent executes the action, and the outcome (as reported by the environment) is printed.
        4.  The new state of the environment after the action is printed.
        5.  There's a brief pause (configurable) between steps to allow observation of the process.

This implementation clearly demonstrates the agent sensing its environment, making a decision based on that sensory input, and then acting upon the environment to change its state.

## How to Run

1.  **Navigate to the project directory**:
    Open your terminal or command prompt.
    ```bash
    cd path/to/your/environment_controlled_agent
    ```

2.  **Ensure all files are present**:
    You should have `agent.py`, `environment.py`, and `main.py` in this directory.

3.  **Run the `main.py` script**:
    ```bash
    python main.py
    ```
    Or, if you have multiple Python versions, you might need to use `python3`:
    ```bash
    python3 main.py
    ```

4.  **Observe the Simulation**:
    The script will run a simulation for a predefined number of steps (default is 6 steps in `main.py`, with a 1.5-second pause between steps). You will see output for each step, detailing:
    *   The state perceived by the agent.
    *   The action chosen by the agent.
    *   The result of that action on the environment.
    *   The new state of the environment.

    **Example Output Snippet (Step 1 might look like this if light is initially off):**
    ```
    --- Environment Controlled Agent Simulation Starting ---
    Agent: EcoBot
    Initial Environment State: {'light_on': False, 'temperature': 20}
    ------------------------------

    --- Step 1/6 ---
    Agent perceives state: {'light_on': False, 'temperature': 20}
    Agent decides to: toggle_light
    Action result: Light turned on.
    New environment state: {'light_on': True, 'temperature': 20}
    (Pausing for 1.5s...)
    ```
    The simulation will continue, showing the agent reacting to the changing temperature (if it goes out of the 18-25 range) or doing nothing if conditions are optimal according to its rules.
