# task_performer.py
import ollama
import random # Kept for potential fallback, though not used in primary LLM paths

DEFAULT_LLM_MODEL = "mistral" # Default model if not specified

def generate_initial_output(prompt: str, llm_model: str = DEFAULT_LLM_MODEL) -> str:
    """
    Generates an initial output based on the prompt using an Ollama LLM.
    """
    generation_prompt = f"Based on the following user prompt, generate a concise initial piece of text, story, plan, or code snippet. Keep it relatively brief as a first draft.\n\nUser Prompt: \"{prompt}\""
    try:
        response = ollama.chat(
            model=llm_model,
            messages=[{'role': 'user', 'content': generation_prompt}]
        )
        initial_text = response['message']['content']
        # print(f"[DEBUG task_performer] Initial LLM Output: {initial_text}")
        return initial_text
    except Exception as e:
        print(f"Error in generate_initial_output with Ollama ({llm_model}): {e}")
        return f"Error generating initial output: {e}. (Original prompt: '{prompt}')"

def refine_output(initial_output: str, critique: str, original_prompt: str, llm_model: str = DEFAULT_LLM_MODEL) -> str:
    """
    Tries to improve the initial output based on the critique using an Ollama LLM.
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
        response = ollama.chat(
            model=llm_model,
            messages=[{'role': 'user', 'content': refinement_prompt}]
        )
        refined_text = response['message']['content']
        # print(f"[DEBUG task_performer] Refined LLM Output: {refined_text}")
        return refined_text
    except Exception as e:
        print(f"Error in refine_output with Ollama ({llm_model}): {e}")
        return f"Error refining output: {e}. (Initial: '{initial_output}', Critique: '{critique}')"

if __name__ == '__main__':
    print("Testing task_performer.py with Ollama...")
    # Ensure Ollama is running: `ollama serve`
    # Ensure the model is pulled: `ollama pull mistral` (or your DEFAULT_LLM_MODEL)

    test_prompts = [
        "write a short story about a curious cat exploring a garden",
        "create a basic 3-step plan for a weekend trip to the beach",
        "write a simple python function to add two numbers"
    ]

    # Using a fixed model for testing here for consistency
    test_llm_model = DEFAULT_LLM_MODEL
    # Or use a specific one known to be good for these tasks if `mistral` is too general
    # test_llm_model = "nous-hermes2"

    for p_text in test_prompts:
        print(f"\n--- Test Prompt: \"{p_text}\" ---")

        print("1. Generating initial output...")
        initial = generate_initial_output(p_text, llm_model=test_llm_model)
        print(f"   Initial Output (from LLM):\n   \"\"\"\n   {initial}\n   \"\"\"")

        # Simulate a critique for testing refine_output
        # In the full agent, this critique will also come from an LLM.
        example_critique = ""
        if "cat" in p_text:
            example_critique = "The story is a bit too short and could use more descriptive language about the garden."
        elif "beach" in p_text:
            example_critique = "The plan is very basic. It should include what to pack and a specific activity."
        elif "python" in p_text:
            example_critique = "The function is okay, but it's missing type hints and a docstring."

        if example_critique:
            print(f"\n2. Refining output with example critique: \"{example_critique}\"")
            refined = refine_output(initial, example_critique, p_text, llm_model=test_llm_model)
            print(f"   Refined Output (from LLM):\n   \"\"\"\n   {refined}\n   \"\"\"")
        else:
            print("\n2. No example critique for this prompt to test refinement.")
        print("-" * 40)
