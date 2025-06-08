# critique_mechanism.py

def critique_output(output: str, prompt: str) -> str:
    """
    Evaluates the output based on simple rules related to the prompt.
    Returns a critique string or "No critique."
    """
    prompt_lower = prompt.lower()
    output_lower = output.lower()

    # Rule 1: Story length
    if "story" in prompt_lower:
        word_count = len(output.split())
        if word_count < 5:
            return "Too short, elaborate more. A good story needs more detail."
        if word_count < 10 and "cat sat on a mat" not in output_lower : # Specific to one refinement
             return "Still a bit brief. Can you expand on the cat's actions or environment?"


    # Rule 2: Travel plan to Paris
    if "plan" in prompt_lower and "trip" in prompt_lower and "paris" in prompt_lower:
        critiques = []
        if "eiffel tower" not in output_lower:
            critiques.append("Missing key landmark: Eiffel Tower.")
        if "louvre" not in output_lower: # Adding another check for Paris
            critiques.append("Missing key landmark: Louvre Museum. Consider adding it.")
        if not critiques:
            if "see things" in output_lower : # If only generic output is present
                return "Plan is too vague. Add specific activities or places for Paris."
            return "No critique." # Only if specific items are mentioned or no obvious omissions
        return " ".join(critiques)

    # Rule 3: Travel plan to Beach
    if "plan" in prompt_lower and "trip" in prompt_lower and "beach" in prompt_lower:
        if "sunscreen" not in output_lower and "towel" not in output_lower:
            return "Missing essential items for a beach trip. What about sunscreen or a towel? Add more steps."
        if len(output.split()) < 5: # If it's just "Find a beach. Relax."
            return "Plan is very basic. Add more steps or details for the beach trip."


    # Rule 4: Python "hello world" code
    if "code" in prompt_lower and "python" in prompt_lower and "hello" in prompt_lower:
        if output == "print('Hello')": # Specifically checking for the incomplete version
            return "Incomplete Python code, missing 'world' part of 'Hello, world!'."
        if "print('hello, world!')" not in output_lower and "print(\"hello, world!\")" not in output_lower:
            return "Python code for 'hello world' seems incorrect or incomplete."

    # Default: No specific critique matched
    return "No critique."

if __name__ == '__main__':
    print("Testing critique_mechanism.py...")

    test_cases = [
        ("write a story about a cat", "A cat sat."),
        ("write a story about a very happy cat", "A cat sat on a fluffy mat, purring softly."),
        ("plan a trip to Paris", "Go to Paris. See things."),
        ("plan a trip to Paris", "Go to Paris. Visit the Eiffel Tower and also go to the Louvre Museum."),
        ("plan a trip to the beach", "Find a beach. Relax."),
        ("plan a trip to the beach", "Find a beach. Relax. Pack sunscreen. Bring a towel. Enjoy the sun."),
        ("code a python hello world", "print('Hello')"),
        ("code a python hello world", "print('Hello, world!')"),
        ("explain quantum physics", "It's complicated.") # Should yield "No critique" based on current rules
    ]

    for prompt_text, output_text in test_cases:
        crit = critique_output(output_text, prompt_text)
        print(f"\nPrompt: {prompt_text}")
        print(f"Output: {output_text}")
        print(f"Critique: {crit}")
