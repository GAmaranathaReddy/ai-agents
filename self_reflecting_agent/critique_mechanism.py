# critique_mechanism.py
import ollama

DEFAULT_LLM_MODEL = "mistral" # Default model if not specified

def critique_output(output_to_critique: str, original_prompt: str, llm_model: str = DEFAULT_LLM_MODEL) -> str:
    """
    Uses an Ollama LLM to evaluate the output based on the original prompt.
    Returns a critique string or "No specific critique points found." if the LLM deems it good.
    """
    critique_prompt_template = f"""Given the original user prompt:
--- User Prompt ---
{original_prompt}
--- End User Prompt ---

And the generated output:
--- Generated Output ---
{output_to_critique}
--- End Generated Output ---

Please evaluate the "Generated Output" based on the "User Prompt". Consider the following:
- Relevance: Does the output address the prompt?
- Completeness: Is the output a complete response to the prompt? (e.g., if a story was asked, is it a story? If a plan, does it have steps?)
- Clarity: Is the output clear and understandable?
- Detail: Is there enough detail, or is it too brief or too verbose?
- Accuracy: If factual information is implied or stated, does it seem plausible (without external checking)?
- Overall Quality: How well does it fulfill the request?

Provide a concise critique focusing on 1-3 specific, actionable points for improvement.
If the output is already very good and closely matches the prompt's intent, you can respond with "No specific critique points found; the output is good."
Your critique should be helpful for revising the output.
"""
    try:
        response = ollama.chat(
            model=llm_model,
            messages=[{'role': 'user', 'content': critique_prompt_template}]
        )
        critique_text = response['message']['content']
        # print(f"[DEBUG critique_mechanism] LLM Critique: {critique_text}")

        # Normalize common "no critique" responses from LLM
        if "no specific critique points found" in critique_text.lower() or \
           "output is good" in critique_text.lower() and len(critique_text) < 100: # Avoid long "good" responses
            return "No critique." # Standardize for the agent

        return critique_text
    except Exception as e:
        print(f"Error in critique_output with Ollama ({llm_model}): {e}")
        return f"Error generating critique: {e}. (Output to critique: '{output_to_critique[:50]}...')"

if __name__ == '__main__':
    print("Testing critique_mechanism.py with Ollama...")
    # Ensure Ollama is running: `ollama serve`
    # Ensure the model is pulled: `ollama pull mistral` (or your DEFAULT_LLM_MODEL)

    test_llm_model = DEFAULT_LLM_MODEL

    test_cases = [
        {
            "prompt": "write a short story about a brave knight saving a village from a dragon",
            "output": "The knight rode.", # Clearly too short
            "expected_critique_keywords": ["short", "detail", "dragon", "village"]
        },
        {
            "prompt": "create a 3-item packing list for a day hike",
            "output": "1. Water\n2. Snacks\n3. Sunscreen\nThis is a good list for hiking.", # Seems good
            "expected_critique_keywords": ["no critique"]
        },
        {
            "prompt": "write a python function that calculates the area of a circle given its radius",
            "output": "def circle_area(r): return 3.14 * r * r", # Good, but could mention math.pi or type hints
            "expected_critique_keywords": ["pi", "type hint", "docstring"] # LLM might suggest these
        },
         {
            "prompt": "Explain the concept of photosynthesis in simple terms.",
            "output": "Photosynthesis is a very important process for plants and life on Earth.", # Too vague
            "expected_critique_keywords": ["explain", "how", "what", "detail"]
        }
    ]

    for case in test_cases:
        print(f"\n--- Test Case ---")
        print(f"Original Prompt: \"{case['prompt']}\"")
        print(f"Output to Critique:\n\"\"\"\n{case['output']}\n\"\"\"")

        critique = critique_output(case['output'], case['prompt'], llm_model=test_llm_model)
        print(f"LLM Critique:\n\"\"\"\n{critique}\n\"\"\"")

        # Simple check if expected keywords are in the critique (case-insensitive)
        if critique and "no critique" not in critique.lower() and "no specific critique points found" not in critique.lower():
            # For actual critiques, check if some expected improvement points are mentioned
            if any(keyword in critique.lower() for keyword in case.get("expected_critique_keywords", [])):
                print("  (Critique seems relevant based on keywords.)")
            else:
                print("  (Critique received, but relevance to expected keywords not automatically confirmed.)")
        elif "no critique" in critique.lower() or "no specific critique points found" in critique.lower():
             if "no critique" in case.get("expected_critique_keywords", []):
                 print("  (Correctly identified as 'No critique'.)")
             else:
                 print("  (LLM found no critique, but test case expected one.)")
        else:
            print("  (Error or unexpected critique format.)")
        print("-" * 40)
