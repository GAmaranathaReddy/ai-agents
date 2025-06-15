# environment.py
from typing import Dict, Any, Optional

class Environment:
    def __init__(self):
        """
        Initializes the environment with default states.
        """
        self.states: Dict[str, Any] = {
            "light_on": False,
            "temperature": 20  # degrees Celsius
        }
        self.valid_actions = ["toggle_light", "set_temperature"]

    def get_state(self) -> Dict[str, Any]:
        """
        Returns the current state of the environment.
        """
        return self.states.copy() # Return a copy to prevent direct modification

    def apply_action(self, action: str, value: Optional[Any] = None) -> str:
        """
        Modifies the environment's state based on the given action.

        Args:
            action (str): The action to apply (e.g., "toggle_light", "set_temperature").
            value (Optional[Any]): The value associated with the action, if any (e.g., temperature value).

        Returns:
            str: A message describing the change that occurred or an error message.
        """
        if action == "toggle_light":
            self.states["light_on"] = not self.states["light_on"]
            status = "on" if self.states["light_on"] else "off"
            return f"Light turned {status}."
        elif action == "set_temperature":
            if value is None:
                return "Error: No value provided for set_temperature action."
            try:
                new_temp = float(value)
                old_temp = self.states["temperature"]
                self.states["temperature"] = new_temp
                return f"Temperature set from {old_temp}°C to {new_temp}°C."
            except ValueError:
                return f"Error: Invalid temperature value '{value}'. Must be a number."
        else:
            return f"Error: Unknown action '{action}'. Valid actions are: {', '.join(self.valid_actions)}."

if __name__ == '__main__':
    print("Testing Environment class...")
    env = Environment()

    print(f"Initial state: {env.get_state()}")

    # Test light toggle
    print(f"Action 'toggle_light': {env.apply_action('toggle_light')}")
    print(f"State after light toggle: {env.get_state()}")
    print(f"Action 'toggle_light': {env.apply_action('toggle_light')}")
    print(f"State after second light toggle: {env.get_state()}")

    # Test temperature setting
    print(f"Action 'set_temperature' (25): {env.apply_action('set_temperature', 25)}")
    print(f"State after temp set: {env.get_state()}")
    print(f"Action 'set_temperature' (15.5): {env.apply_action('set_temperature', 15.5)}")
    print(f"State after temp set: {env.get_state()}")

    # Test error cases
    print(f"Action 'set_temperature' (no value): {env.apply_action('set_temperature')}")
    print(f"Action 'set_temperature' (bad value 'abc'): {env.apply_action('set_temperature', 'abc')}")
    print(f"Action 'unknown_action': {env.apply_action('unknown_action')}")

    print(f"Final state: {env.get_state()}")
