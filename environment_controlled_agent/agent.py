# agent.py
from typing import Dict, Any, Tuple, Optional
from environment import Environment
# import ollama # No longer directly importing ollama
from common import get_llm_provider_instance # Use the abstraction layer
import json

class EnvironmentControlledAgent:
    def __init__(self, environment: Environment): # llm_model parameter removed
        """
        Initializes the agent with a reference to an environment.
        LLM provider is determined by global configuration.
        Args:
            environment (Environment): An instance of the Environment class.
        """
        self.environment = environment
        self.llm_provider = get_llm_provider_instance()
        self.name = f"EcoBot (using {type(self.llm_provider).__name__})"
        # self.llm_model = llm_model # Removed, provider handles its own model config
        self.current_goal = "Maintain a balanced and comfortable environment: light should ideally be on, and temperature should be between 18 and 25 degrees Celsius. Prioritize turning on the light if it's off."
        self.last_explanation = "No decision made yet." # Will store explanation from LLM

    def set_goal(self, natural_language_goal: str) -> str:
        """Sets a new goal for the agent in natural language."""
        self.current_goal = natural_language_goal
        confirmation_message = f"New goal set: {self.current_goal}"
        self.last_explanation = confirmation_message # Update last explanation to reflect goal change
        return confirmation_message

    def perceive(self) -> Dict[str, Any]:
        """
        Perceives the current state of the environment.

        Returns:
            Dict[str, Any]: The current state of the environment.
        """
        return self.environment.get_state()

    def decide_action(self, current_state: Dict[str, Any]) -> Tuple[str, Optional[Any]]:
        """
        Decides an action based on the current environment state and its current goal using an LLM.

        Args:
            current_state (Dict[str, Any]): The current state of the environment.

        Returns:
            Tuple[str, Optional[Any], str]: A tuple containing the action string,
                                            an optional value for that action,
                                            and an explanation for the decision.
        """
        available_actions_desc = {
            "toggle_light": "Toggles the current light status (on/off). No value needed.",
            "set_temperature": "Sets the temperature to a specific VALUE. Expects a numerical value.",
            "do_nothing": "Take no action if the goal is met or no useful action can be taken."
        }
        actions_prompt_info = "\n".join([f"- '{name}': {desc}" for name, desc in available_actions_desc.items()])

        prompt_to_llm = f"""Current Goal: "{self.current_goal}"

Current Environment State:
{json.dumps(current_state)}

Available Actions:
{actions_prompt_info}

Based on the current goal and environment state, choose the single best action to take next to progress towards the goal.
Provide your response as a JSON object with three keys:
1. "action_name": The name of the chosen action (must be one of: {', '.join(available_actions_desc.keys())}).
2. "action_value": The value for the action, if applicable (e.g., the temperature for 'set_temperature'). If no value is needed, set this to null.
3. "explanation": A brief explanation of why you chose this action in relation to the goal and state.

Example for setting temperature: {{"action_name": "set_temperature", "action_value": 22, "explanation": "Temperature is too low for comfort."}}
Example for toggling light: {{"action_name": "toggle_light", "action_value": null, "explanation": "Light is currently off and goal implies it should be on."}}
Example for no action: {{"action_name": "do_nothing", "action_value": null, "explanation": "The environment is currently optimal according to the goal."}}

Only provide the JSON response.
"""
        try:
            # print(f"[DEBUG AGENT] Prompt to LLM:\n{prompt_to_llm}") # For debugging
            # response = ollama.chat( # Old call
            #     model=self.llm_model,
            #     messages=[{'role': 'user', 'content': prompt_to_llm}],
            #     format='json'
            # )
            # llm_output_str = response['message']['content']
            llm_output_str = self.llm_provider.chat(
                messages=[{'role': 'user', 'content': prompt_to_llm}],
                request_json_output=True # Signal to provider to request JSON
            )
            # print(f"[DEBUG AGENT] Raw LLM Output: {llm_output_str}") # For debugging
            # Provider should raise error if JSON was requested but not received (for providers that support enforced JSON mode).
            # For others, it's best effort via prompt, so json.loads might fail here.
            llm_output = json.loads(llm_output_str)

            action_name = llm_output.get("action_name", "do_nothing")
            action_value = llm_output.get("action_value") # Can be None/null
            explanation = llm_output.get("explanation", "No explanation provided by LLM.")

            self.last_explanation = explanation # Store for UI or logging

            # Validate action_name
            if action_name not in available_actions_desc:
                self.last_explanation = f"LLM chose an invalid action ('{action_name}'). Defaulting to 'do_nothing'."
                action_name = "do_nothing"
                action_value = None

            # Ensure action_value is None if not applicable (e.g. for toggle_light, do_nothing)
            if action_name in ["toggle_light", "do_nothing"]:
                action_value = None
            elif action_name == "set_temperature":
                if not isinstance(action_value, (int, float)):
                    self.last_explanation = f"LLM provided invalid value '{action_value}' for set_temperature. Defaulting to 'do_nothing'."
                    action_name = "do_nothing"
                    action_value = None

            return action_name, action_value, self.last_explanation

        except json.JSONDecodeError as e:
            error_msg = f"LLM output was not valid JSON: {e}. Raw output from provider: {llm_output_str}"
            print(f"[ERROR AGENT] {error_msg}")
            self.last_explanation = error_msg
            return "do_nothing", None, self.last_explanation
        except Exception as e:
            error_msg = f"LLM provider error ({type(self.llm_provider).__name__}): {type(e).__name__} - {e}."
            print(f"[ERROR AGENT] {error_msg}")
            self.last_explanation = error_msg
            return "do_nothing", None, self.last_explanation

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
