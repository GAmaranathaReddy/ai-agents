# agent.py
from task_performer import generate_initial_output, refine_output # These will now take llm_provider
from critique_mechanism import critique_output # This will now take llm_provider
from common import get_llm_provider_instance # Use the abstraction layer

class SelfReflectingAgent:
    def __init__(self): # LLM model is now configured via the provider
        self.llm_provider = get_llm_provider_instance()
        self.name = f"ReflectorBot (using {type(self.llm_provider).__name__})"
        self.max_refinement_cycles = 1 # Control how many times it tries to refine
        # self.llm_model = llm_model # Removed, provider handles its own model config

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
        results["log"].append(f"Task: Generating initial output for prompt: \"{user_prompt}\" using provider: {type(self.llm_provider).__name__}")
        current_output = generate_initial_output(user_prompt, llm_provider=self.llm_provider)
        results["initial_output"] = current_output
        results["log"].append(f"LLM Provider (Initial Output) said: '{current_output[:100]}...'")


        # Self-reflection loop (limited by max_refinement_cycles)
        for i in range(self.max_refinement_cycles):
            results["log"].append(f"Reflection cycle {i+1}/{self.max_refinement_cycles}...")

            # 2. Critique the current output
            results["log"].append(f"Task: Critiquing output: \"{current_output[:100]}...\" using provider: {type(self.llm_provider).__name__}")
            critique = critique_output(current_output, user_prompt, llm_provider=self.llm_provider)
            results["critique"] = critique # Store the last critique
            results["log"].append(f"LLM Provider (Critique) said: '{critique[:100]}...'")

            # 3. Refine if there's a meaningful critique
            if critique.strip().lower() != "no critique.":
                results["log"].append(f"Task: Refining output based on critique using provider: {type(self.llm_provider).__name__}")
                refined_version = refine_output(current_output, critique, user_prompt, llm_provider=self.llm_provider)
                results["log"].append(f"LLM Provider (Refined Output) said: '{refined_version[:100]}...'")

                # Check if refinement actually changed something
                if refined_version == current_output:
                    results["log"].append("Refinement did not significantly change the output. Stopping reflection.")
                    results["refined_output"] = refined_version # Store it anyway
                    current_output = refined_version # Though it's same, for consistency
                    break

                current_output = refined_version
                results["refined_output"] = current_output # Update refined output
            else:
                results["log"].append("No meaningful critique received. Stopping reflection.")
                results["refined_output"] = current_output # Final output is the same as current if no refinement done
                break # No critique, so no need to refine further

        results["final_output"] = current_output
        return results

if __name__ == '__main__':
    # Ensure Ollama is running and the model (e.g., "mistral") is pulled.
    # Example: ollama pull mistral
    agent = SelfReflectingAgent() # Uses default "mistral"
    # agent = SelfReflectingAgent(llm_model="nous-hermes2") # Example with another model

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
