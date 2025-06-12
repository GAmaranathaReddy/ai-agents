# task_performer.py
# import ollama # No longer directly using ollama
from common.llm_providers import BaseLLMProvider # Import the base class for type hinting
import random # Kept for potential fallback, though not used in primary LLM paths

# DEFAULT_LLM_MODEL = "mistral" # Default model is now handled by the provider config

def generate_initial_output(prompt: str, llm_provider: BaseLLMProvider) -> str:
    """
    Generates an initial output based on the prompt using the provided LLM provider.
    """
    generation_prompt = f"Based on the following user prompt, generate a concise initial piece of text, story, plan, or code snippet. Keep it relatively brief as a first draft.\n\nUser Prompt: \"{prompt}\""
    try:
        # response = ollama.chat( # Old call
        #     model=llm_model,
        #     messages=[{'role': 'user', 'content': generation_prompt}]
        # )
        # initial_text = response['message']['content']
        initial_text = llm_provider.chat(
            messages=[{'role': 'user', 'content': generation_prompt}]
        )
        # print(f"[DEBUG task_performer] Initial LLM Output: {initial_text}")
        return initial_text
    except Exception as e:
        # print(f"Error in generate_initial_output with Ollama ({llm_model}): {e}")
        print(f"Error in generate_initial_output with {type(llm_provider).__name__}: {e}")
        return f"Error generating initial output: {e}. (Original prompt: '{prompt}')"

def refine_output(initial_output: str, critique: str, original_prompt: str, llm_provider: BaseLLMProvider) -> str:
    """
    Tries to improve the initial output based on the critique using the provided LLM provider.
    """
    refinement_prompt = f"""The user's original request was: "{original_prompt}"
The initial output generated was:
--- Initial Output ---
{initial_output}
--- End Initial Output ---

A critique of this initial output was provided:
--- Critique ---
{critique}
--- End Critique ---

Please generate a revised and improved version of the output that directly addresses all points in the critique and better fulfills the original user request.
If the critique is "No critique." or seems unhelpful, try to improve the initial output based on the original prompt in a general way (e.g. by adding more detail or making it more complete).
"""
    try:
        # response = ollama.chat( # Old call
        #     model=llm_model,
        #     messages=[{'role': 'user', 'content': refinement_prompt}]
        # )
        # refined_text = response['message']['content']
        refined_text = llm_provider.chat(
            messages=[{'role': 'user', 'content': refinement_prompt}]
        )
        # print(f"[DEBUG task_performer] Refined LLM Output: {refined_text}")
        return refined_text
    except Exception as e:
        # print(f"Error in refine_output with Ollama ({llm_model}): {e}")
        print(f"Error in refine_output with {type(llm_provider).__name__}: {e}")
        return f"Error refining output: {e}. (Initial: '{initial_output}', Critique: '{critique}')"

if __name__ == '__main__':
    print("Testing task_performer.py with the common LLM provider...")
    # This test now requires environment variables for LLM_PROVIDER to be set up
    # (e.g., LLM_PROVIDER="ollama", OLLAMA_MODEL="mistral")
    # and the respective service (e.g., Ollama) to be running.

    from common import get_llm_provider_instance # For testing

    try:
        test_provider = get_llm_provider_instance()
        print(f"Using LLM provider: {type(test_provider).__name__} with model: {test_provider.default_model}")

        test_prompts = [
            "write a short story about a curious cat exploring a garden",
            "create a basic 3-step plan for a weekend trip to the beach",
            "write a simple python function to add two numbers"
        ]

        for p_text in test_prompts:
            print(f"\n--- Test Prompt: \"{p_text}\" ---")

            print("1. Generating initial output...")
            initial = generate_initial_output(p_text, llm_provider=test_provider)
            print(f"   Initial Output (from LLM):\n   \"\"\"\n   {initial}\n   \"\"\"")

            example_critique = ""
            if "cat" in p_text:
                example_critique = "The story is a bit too short and could use more descriptive language about the garden."
            elif "beach" in p_text:
                example_critique = "The plan is very basic. It should include what to pack and a specific activity."
            elif "python" in p_text:
                example_critique = "The function is okay, but it's missing type hints and a docstring."

            if example_critique and not initial.startswith("Error generating initial output"):
                print(f"\n2. Refining output with example critique: \"{example_critique}\"")
                refined = refine_output(initial, example_critique, p_text, llm_provider=test_provider)
                print(f"   Refined Output (from LLM):\n   \"\"\"\n   {refined}\n   \"\"\"")
            elif initial.startswith("Error generating initial output"):
                print("\n2. Skipping refinement due to error in initial generation.")
            else:
                print("\n2. No example critique for this prompt to test refinement.")
            print("-" * 40)

    except Exception as e:
        print(f"Could not run task_performer test: {e}")
        print("Ensure your LLM_PROVIDER environment variables are set and the service is running.")
