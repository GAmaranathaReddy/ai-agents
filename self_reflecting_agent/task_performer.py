# task_performer.py
import random

def generate_initial_output(prompt: str) -> str:
    """
    Generates a basic initial output based on the prompt.
    Simulates a first-pass attempt at a task.
    """
    prompt_lower = prompt.lower()
    if "story" in prompt_lower and "cat" in prompt_lower:
        return "A cat sat."
    elif "story" in prompt_lower and "dog" in prompt_lower:
        return "A dog barked."
    elif "plan" in prompt_lower and "trip" in prompt_lower and "paris" in prompt_lower:
        return "Go to Paris. See things."
    elif "plan" in prompt_lower and "trip" in prompt_lower and "beach" in prompt_lower:
        return "Find a beach. Relax."
    elif "code" in prompt_lower and "python" in prompt_lower and "hello" in prompt_lower:
        return "print('Hello')" # Intentionally incomplete for critique
    else:
        return f"Initial thought on '{prompt}': It's an interesting topic."

def refine_output(initial_output: str, critique: str, prompt: str = "") -> str:
    """
    Tries to improve the initial output based on the critique.
    Simulates a refinement step.
    """
    critique_lower = critique.lower()
    refined_output = initial_output

    if "too short" in critique_lower:
        if "cat sat" in initial_output:
            refined_output += " The cat sat on a fluffy mat, purring softly."
        elif "dog barked" in initial_output:
            refined_output += " The dog barked at a squirrel that ran up a tree."
        else:
            refined_output += " More details could be added here to make it longer."

    if "missing key landmark: eiffel tower" in critique_lower:
        if "go to paris" in initial_output.lower():
            refined_output += " Definitely visit the Eiffel Tower for great views."
        else: # Should not happen if critique is accurate
            refined_output += " (Refinement: The Eiffel Tower is a key landmark in Paris.)"

    if "missing key landmark: Louvre Museum" in critique_lower: # Example of another landmark
        if "go to paris" in initial_output.lower():
            refined_output += " Also, consider visiting the Louvre Museum."

    if "incomplete python code" in critique_lower and "print('Hello')" in initial_output:
        refined_output = "print('Hello, world!') # Added the missing part of the string and a comment."

    if "add more steps" in critique_lower and "beach" in initial_output.lower():
        refined_output += " Pack sunscreen. Bring a towel. Enjoy the sun."

    # If no specific refinement rule matches, but there was a critique, add a generic note
    if refined_output == initial_output and critique != "No critique.":
        refined_output += f" (Self-note: Addressed critique: '{critique}')"

    return refined_output

if __name__ == '__main__':
    print("Testing task_performer.py...")

    prompts_outputs = {
        "write a story about a cat": "",
        "plan a trip to Paris": "",
        "code a python hello world": ""
    }

    for p in prompts_outputs:
        print(f"\nPrompt: {p}")
        initial = generate_initial_output(p)
        print(f"Initial: {initial}")

        # Simulate critiques for testing refine_output
        if "cat" in p:
            crit = "Too short, elaborate more."
            refined = refine_output(initial, crit)
            print(f"Critique: {crit}")
            print(f"Refined: {refined}")
        elif "Paris" in p:
            crit = "Missing key landmark: Eiffel Tower."
            refined = refine_output(initial, crit)
            print(f"Critique: {crit}")
            print(f"Refined: {refined}")
        elif "python" in p:
            crit = "Incomplete Python code, missing 'world'."
            refined = refine_output(initial, crit, p) # Pass prompt for context
            print(f"Critique: {crit}")
            print(f"Refined: {refined}")
