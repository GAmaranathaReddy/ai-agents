# Self-Reflecting Agent

## Self-Reflecting Agent Pattern

A Self-Reflecting Agent is designed to improve its performance or output through a process of internal evaluation and refinement. Instead of producing a final output in a single pass, it engages in a loop that typically involves:

1.  **Generation**: The agent produces an initial version of the output or a plan of action based on the given prompt or task.
2.  **Evaluation/Critique**: The agent (or a component of it) analyzes this initial output against a set of criteria, rules, or desired qualities. This step identifies flaws, shortcomings, or areas for improvement, resulting in a "critique."
3.  **Refinement/Self-Correction**: Based on the critique, the agent attempts to modify or regenerate its output to address the identified issues. This leads to a revised version.

This loop can, in theory, run multiple times, with each iteration aiming to enhance the quality of the output. The goal is to achieve a more accurate, complete, or polished result than what might be possible with a single-pass generation process. This pattern mimics the human tendency to review and revise work.

## Implementation

This project provides a simplified demonstration of the Self-Reflecting Agent pattern:

1.  **`task_performer.py`**:
    *   `generate_initial_output(prompt: str)`: This function simulates the initial generation phase. Given a user prompt, it produces a very basic, often incomplete, first draft of an output. For instance, for "write a story about a cat," it might return "A cat sat."
    *   `refine_output(initial_output: str, critique: str, prompt: str)`: This function simulates the refinement phase. It takes the initial output and the critique (and optionally the original prompt for context) and tries to modify the output to address the critique. For example, if the critique is "Too short," it might append more text.

2.  **`critique_mechanism.py`**:
    *   `critique_output(output: str, prompt: str)`: This function acts as the evaluation or critique component. It takes the current output and the original prompt and applies a set of simple, hardcoded rules to identify flaws.
        *   Example rule: If the prompt was "write a story..." and the output has fewer than 5 words, it generates the critique "Too short, elaborate more."
        *   Example rule: If the prompt was "plan a trip to Paris" and the output doesn't mention "Eiffel Tower," it critiques "Missing key landmark: Eiffel Tower."
        *   If no predefined rules detect an issue, it returns "No critique."

3.  **`agent.py`**:
    *   Defines the `SelfReflectingAgent` class.
    *   Its `process_request(user_prompt: str)` method orchestrates the self-reflection loop:
        1.  It calls `generate_initial_output()` with the `user_prompt` to get the first draft.
        2.  It then calls `critique_output()` to evaluate this draft.
        3.  If the critique is anything other than "No critique.", it calls `refine_output()` to attempt to improve the draft based on the feedback.
        4.  The agent is currently set for one cycle of refinement (`max_refinement_cycles = 1`).
        5.  It collects the initial output, critique, and the refined output (if any) to show the user the process.

4.  **`main.py`**:
    *   Provides a simple command-line interface (CLI) to interact with the `SelfReflectingAgent`.
    *   The user inputs a prompt, and the CLI displays the sequence of initial output, critique, and refined output, illustrating the agent's internal reflection process.

This implementation demonstrates the core cycle: an initial attempt (`generate_initial_output`), an evaluation of that attempt (`critique_output`), and an effort to improve based on that evaluation (`refine_output`).

## How to Run

1.  **Navigate to the project directory**:
    Open your terminal or command prompt.
    ```bash
    cd path/to/your/self_reflecting_agent
    ```

2.  **Ensure all files are present**:
    You should have `agent.py`, `task_performer.py`, `critique_mechanism.py`, and `main.py` in this directory.

3.  **Run the `main.py` script**:
    ```bash
    python main.py
    ```
    Or, if you have multiple Python versions, you might need to use `python3`:
    ```bash
    python3 main.py
    ```

4.  **Interact with the Agent**:
    The CLI will start. Type your prompt and press Enter.

    **Example Interaction**:
    ```
    Self-Reflecting Agent CLI
    Powered by: ReflectorBot
    Type a prompt for the agent (e.g., 'write a story about a cat', 'plan a trip to Paris').
    Type 'exit' or 'quit' to stop.
    ------------------------------
    You: write a story about a cat

    Agent is thinking...

    --- Reflection Process ---
    Prompt: "write a story about a cat"
    1. Initial Output: "A cat sat."
    2. Critique: "Too short, elaborate more. A good story needs more detail."
    3. Refined Output: "A cat sat. The cat sat on a fluffy mat, purring softly."
    --- End of Process ---
    Final Agent Output: "A cat sat. The cat sat on a fluffy mat, purring softly."

    ------------------------------
    You: plan a trip to Paris

    Agent is thinking...

    --- Reflection Process ---
    Prompt: "plan a trip to Paris"
    1. Initial Output: "Go to Paris. See things."
    2. Critique: "Missing key landmark: Eiffel Tower. Missing key landmark: Louvre Museum. Consider adding it. Plan is too vague. Add specific activities or places for Paris."
    3. Refined Output: "Go to Paris. See things. Definitely visit the Eiffel Tower for great views. Also, consider visiting the Louvre Museum."
    --- End of Process ---
    Final Agent Output: "Go to Paris. See things. Definitely visit the Eiffel Tower for great views. Also, consider visiting the Louvre Museum."

    ------------------------------
    You: exit
    Exiting agent CLI. Goodbye!
    ```

### Web UI (Streamlit)

The Self-Reflecting Agent also includes a web-based user interface built with Streamlit, which visually demonstrates its generate-critique-refine process.

1.  **Install Streamlit**:
    If you haven't installed it yet, you'll need Streamlit. If your main project utilizes Poetry, consider adding Streamlit as a dependency. For a standard local installation:
    ```bash
    pip install streamlit
    ```

2.  **Run the Streamlit App**:
    To launch the web UI, open your terminal, navigate to the root directory of this repository (where the main `README.md` is located), and run the command:
    ```bash
    streamlit run self_reflecting_agent/app_ui.py
    ```
    This will typically open the application in your default web browser.

3.  **Interact with the Agent via Web**:
    *   The web interface will feature a title, a brief description, and a text input field for your prompt.
    *   A sidebar will offer example prompts that the agent is designed to handle (e.g., simple story writing or plan generation).
    *   Enter your prompt (e.g., "write a story about a cat", "plan a trip to Paris").
    *   Click the "Process Prompt" button.
    *   The UI will then display:
        *   The "Initial Output" generated by the agent.
        *   The "Critique" produced by the agent's evaluation mechanism.
        *   The "Refined Output" after the agent attempts to address the critique.
        *   The "Final Output" of the agent.
        *   An expandable section to "View Agent's Internal Log" for more detailed steps.
    This allows for a clear view of the agent's multi-step self-reflection process.
