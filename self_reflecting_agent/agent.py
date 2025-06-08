# agent.py
from task_performer import generate_initial_output, refine_output
from critique_mechanism import critique_output

class SelfReflectingAgent:
    def __init__(self):
        self.name = "ReflectorBot"
        self.max_refinement_cycles = 1 # Control how many times it tries to refine

    def process_request(self, user_prompt: str) -> dict:
        """
        Processes the user's prompt through a cycle of generation, critique, and refinement.

        Returns:
            A dictionary containing the initial output, critique, and refined output (if any).
        """
        results = {
            "prompt": user_prompt,
            "initial_output": None,
            "critique": None,
            "refined_output": None,
            "final_output": None,
            "log": []
        }

        # 1. Generate initial output
        current_output = generate_initial_output(user_prompt)
        results["initial_output"] = current_output
        results["log"].append(f"Generated initial output: '{current_output}'")

        # Self-reflection loop (limited by max_refinement_cycles)
        for i in range(self.max_refinement_cycles):
            results["log"].append(f"Reflection cycle {i+1}...")

            # 2. Critique the current output
            critique = critique_output(current_output, user_prompt)
            results["critique"] = critique # Store the last critique
            results["log"].append(f"Critique received: '{critique}'")

            # 3. Refine if there's a meaningful critique
            if critique != "No critique.":
                refined_version = refine_output(current_output, critique, user_prompt)
                results["log"].append(f"Refined output based on critique: '{refined_version}'")

                # Check if refinement actually changed something to avoid infinite loops on poor refinement logic
                if refined_version == current_output:
                    results["log"].append("Refinement did not change the output. Stopping reflection.")
                    results["refined_output"] = refined_version # Store it anyway
                    current_output = refined_version
                    break

                current_output = refined_version
                results["refined_output"] = current_output # Update refined output
            else:
                results["log"].append("No critique received or critique was 'No critique.'. Stopping reflection.")
                break # No critique, so no need to refine further

        results["final_output"] = current_output
        return results

if __name__ == '__main__':
    agent = SelfReflectingAgent()

    test_prompts = [
        "write a story about a cat",
        "plan a trip to Paris",
        "code a python hello world",
        "write a story about a dog", # Will get "Too short" then refined
        "plan a trip to the beach" # Will get "Missing essentials" then refined
    ]

    for prompt in test_prompts:
        print(f"\n--- Processing Prompt: \"{prompt}\" ---")
        reflection_results = agent.process_request(prompt)

        print(f"  Prompt: {reflection_results['prompt']}")
        print(f"  Initial Output: {reflection_results['initial_output']}")
        print(f"  Critique: {reflection_results['critique']}")

        if reflection_results['refined_output'] and reflection_results['refined_output'] != reflection_results['initial_output']:
            print(f"  Refined Output: {reflection_results['refined_output']}")
        elif reflection_results['critique'] != "No critique.":
             print(f"  Refined Output: (No change after refinement or refinement matched initial)")

        print(f"  Final Output: {reflection_results['final_output']}")
        # print(f"  Log:")
        # for entry in reflection_results['log']:
        #     print(f"    - {entry}")
        print("-" * 40)
