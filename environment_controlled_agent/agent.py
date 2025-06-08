# agent.py
from typing import Dict, Any, Tuple, Optional
from environment import Environment # Assuming environment.py is in the same directory

class EnvironmentControlledAgent:
    def __init__(self, environment: Environment):
        """
        Initializes the agent with a reference to an environment.

        Args:
            environment (Environment): An instance of the Environment class.
        """
        self.environment = environment
        self.name = "EcoBot"

    def perceive(self) -> Dict[str, Any]:
        """
        Perceives the current state of the environment.

        Returns:
            Dict[str, Any]: The current state of the environment.
        """
        return self.environment.get_state()

    def decide_action(self, current_state: Dict[str, Any]) -> Tuple[str, Optional[Any]]:
        """
        Decides an action based on the current environment state.

        Args:
            current_state (Dict[str, Any]): The current state of the environment.

        Returns:
            Tuple[str, Optional[Any]]: A tuple containing the action string
                                       and an optional value for that action.
                                       Example: ("toggle_light", None) or ("set_temperature", 22).
        """
        light_on = current_state.get("light_on")
        temperature = current_state.get("temperature")

        if light_on == False: # Explicitly check for False, as None could be an issue
            return "toggle_light", None

        if temperature is not None: # Ensure temperature is not None before comparing
            if temperature < 18:
                return "set_temperature", 22
            elif temperature > 25:
                return "set_temperature", 22

        return "do_nothing", None # Default action if no other conditions are met

    def execute_action(self, action: str, value: Optional[Any] = None) -> str:
        """
        Executes the chosen action on the environment.

        Args:
            action (str): The action to execute.
            value (Optional[Any]): The value associated with the action, if any.

        Returns:
            str: A message describing the result of the action from the environment.
        """
        if action == "do_nothing":
            return f"{self.name} decided to do nothing."
        return self.environment.apply_action(action, value)

if __name__ == '__main__':
    print("Testing EnvironmentControlledAgent...")

    # Create an environment instance
    env = Environment()
    agent = EnvironmentControlledAgent(env)
    print(f"Agent '{agent.name}' initialized with environment.")

    # --- Test Case 1: Light is off ---
    print("\n--- Test Case 1: Light is off ---")
    env.states["light_on"] = False
    env.states["temperature"] = 20
    current_state_1 = agent.perceive()
    print(f"Perceived state: {current_state_1}")
    action_1, value_1 = agent.decide_action(current_state_1)
    print(f"Decided action: {action_1}, Value: {value_1}")
    result_1 = agent.execute_action(action_1, value_1)
    print(f"Execution result: {result_1}")
    print(f"Environment state after action: {env.get_state()}")

    # --- Test Case 2: Temperature is too low (light is now on) ---
    print("\n--- Test Case 2: Temperature too low ---")
    # env.states["light_on"] = True # Set by previous action
    env.states["temperature"] = 15
    current_state_2 = agent.perceive()
    print(f"Perceived state: {current_state_2}")
    action_2, value_2 = agent.decide_action(current_state_2)
    print(f"Decided action: {action_2}, Value: {value_2}")
    result_2 = agent.execute_action(action_2, value_2)
    print(f"Execution result: {result_2}")
    print(f"Environment state after action: {env.get_state()}")

    # --- Test Case 3: Temperature is too high ---
    print("\n--- Test Case 3: Temperature too high ---")
    env.states["temperature"] = 30
    current_state_3 = agent.perceive()
    print(f"Perceived state: {current_state_3}")
    action_3, value_3 = agent.decide_action(current_state_3)
    print(f"Decided action: {action_3}, Value: {value_3}")
    result_3 = agent.execute_action(action_3, value_3)
    print(f"Execution result: {result_3}")
    print(f"Environment state after action: {env.get_state()}")

    # --- Test Case 4: Everything is fine (light on, temp normal) ---
    print("\n--- Test Case 4: Optimal conditions ---")
    # env.states["light_on"] = True
    # env.states["temperature"] = 22 # Set by previous action
    current_state_4 = agent.perceive()
    print(f"Perceived state: {current_state_4}")
    action_4, value_4 = agent.decide_action(current_state_4)
    print(f"Decided action: {action_4}, Value: {value_4}")
    result_4 = agent.execute_action(action_4, value_4) # Should be "do_nothing"
    print(f"Execution result: {result_4}")
    print(f"Environment state after action: {env.get_state()}")
