# main.py
import time
from environment import Environment
from agent import EnvironmentControlledAgent

def run_simulation(steps: int = 10, delay_between_steps: float = 1.0):
    """
    Runs a simulation loop for the Environment-Controlled Agent.

    Args:
        steps (int): The number of steps to run the simulation for.
        delay_between_steps (float): Time in seconds to pause between steps.
    """
    env = Environment()
    agent = EnvironmentControlledAgent(env)

    print("--- Environment Controlled Agent Simulation Starting ---")
    print(f"Agent: {agent.name}")
    print(f"Initial Environment State: {env.get_state()}")
    print("-" * 30)

    for i in range(steps):
        print(f"\n--- Step {i + 1}/{steps} ---")

        # 1. Agent perceives the environment state
        current_state = agent.perceive()
        print(f"Agent perceives state: {current_state}")

        # 2. Agent decides an action
        action, value, explanation = agent.decide_action(current_state) # Now returns explanation

        decision_str = f"Agent decides to: {action}"
        if value is not None:
            decision_str += f" with value {value}"
        print(decision_str)
        print(f"Agent's reasoning: \"{explanation}\"")

        # 3. Agent executes the action
        action_result = agent.execute_action(action, value)
        print(f"Action execution result: {action_result}")

        # Display the new environment state
        new_env_state = env.get_state()
        print(f"New environment state: {new_env_state}")

        # Small logic to change environment state externally for more dynamic simulation
        # This is just to make the simulation more interesting if the agent reaches its goal quickly.
        if i % 3 == 0 and i > 0 : # Every 3 steps after the first
            if new_env_state["light_on"]:
                print("SIM_UPDATE: External event toggles light OFF.")
                env.apply_action("toggle_light")
            elif new_env_state["temperature"] == 22:
                 new_temp_external = random.choice([15, 28])
                 print(f"SIM_UPDATE: External event sets temperature to {new_temp_external}°C.")
                 env.apply_action("set_temperature", new_temp_external)


        if i < steps - 1: # Don't pause after the last step
            if delay_between_steps > 0:
                print(f"(Pausing for {delay_between_steps}s...)")
                time.sleep(delay_between_steps)
            else: # If no delay, at least allow manual progression
                input("Press Enter to proceed to the next step...") # pragma: no cover

    print("\n--- Simulation Ended ---")
    print(f"Final Environment State: {env.get_state()}")

if __name__ == "__main__":
    import random # For the SIM_UPDATE logic
    # You can change the number of steps or delay here
    # For automated testing, a small delay or 0 might be preferred.
    # For manual observation, a longer delay or input-based progression is better.

    # Example: run_simulation(steps=5, delay_between_steps=2)
    # Example: run_simulation(steps=10, delay_between_steps=0) # Press Enter to advance
    run_simulation(steps=8, delay_between_steps=2)
