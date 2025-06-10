# Self-Reflecting Agent

## Self-Reflecting Agent (LLM-Powered)

A Self-Reflecting Agent improves its output through a cycle of generation, evaluation (critique), and refinement. This version is **fully LLM-powered**, using Ollama for each stage of this process.

1.  **Generation**: Given a user prompt, an LLM generates an initial draft.
2.  **Critique**: A second LLM call evaluates this draft against the original prompt, providing specific feedback for improvement.
3.  **Refinement**: A third LLM call takes the original draft, the critique, and the initial prompt, and attempts to produce a revised output that addresses the critique.

This cycle aims to produce higher-quality, more nuanced results than a single LLM call might achieve.

## Implementation

This project demonstrates the fully LLM-driven Self-Reflecting Agent pattern:

1.  **`task_performer.py` (Updated)**:
    *   `generate_initial_output(prompt: str, llm_model: str)`: Calls the specified Ollama `llm_model` with the user `prompt` to produce a first draft. The prompt to the LLM is engineered to ask for a concise initial piece of text.
    *   `refine_output(initial_output: str, critique: str, original_prompt: str, llm_model: str)`: Takes the `initial_output`, `critique`, and `original_prompt`. It constructs a new prompt for the Ollama `llm_model`, instructing it to generate a revised version of the output that addresses all points in the critique and better fulfills the original request.

2.  **`critique_mechanism.py` (Updated)**:
    *   `critique_output(output_to_critique: str, original_prompt: str, llm_model: str)`: Uses the specified Ollama `llm_model` to evaluate the `output_to_critique` based on the `original_prompt`. The prompt to the LLM asks it to consider relevance, completeness, clarity, detail, and overall quality, and to provide 1-3 specific, actionable critique points or state that the output is good. It normalizes common "no critique" LLM responses to a standard "No critique." string.

3.  **`agent.py` (`SelfReflectingAgent` class - Updated)**:
    *   Initialized with an `llm_model` name (e.g., "mistral"), which is passed to all component functions.
    *   The `process_request(user_prompt: str)` method orchestrates the LLM-driven self-reflection loop:
        1.  Calls `generate_initial_output()` to get the LLM-generated first draft.
        2.  Calls `critique_output()` to get an LLM-generated critique of that draft.
        3.  If the critique is meaningful (not "No critique."), it calls `refine_output()` to get an LLM-generated revised version.
        4.  The agent logs these LLM interactions and returns a structured dictionary with `user_prompt`, `initial_output`, `critique`, `refined_output`, `final_output`, and a `log` of operations.

4.  **`main.py` (CLI)** and **`app_ui.py` (Streamlit UI)**:
    *   These interfaces interact with the LLM-powered `SelfReflectingAgent`.
    *   The Streamlit UI is particularly useful for visualizing the distinct LLM-generated outputs for each stage (initial draft, critique, refinement).

## Prerequisites & Setup

1.  **Ollama and LLM Model**:
    *   **Install Ollama**: Ensure Ollama is installed and running. See the [Ollama official website](https://ollama.com/).
    *   **Pull an LLM Model**: The agent defaults to `"mistral"`. You need this model (or your chosen alternative) pulled in Ollama.
      ```bash
      ollama pull mistral
      ```
      A model good at instruction-following is recommended for all stages (generation, critique, and refinement).
    *   **Install Ollama Python Client**:
      ```bash
      pip install ollama
      ```

2.  **Streamlit (for UI)**:
    *   If you want to use the web UI, install Streamlit:
      ```bash
      pip install streamlit
      ```

*(If using Poetry for the main project, add `ollama` and `streamlit` to your `pyproject.toml` and run `poetry install`.)*

## How to Run

**(Ensure you have completed all Prerequisites & Setup steps above: Ollama running, model pulled, and Python packages installed.)**

### 1. Command-Line Interface (CLI)

1.  **Navigate to the agent's directory**:
    ```bash
    cd path/to/your/self_reflecting_agent
    ```

2.  **Run the `main.py` script**:
    ```bash
    python main.py
    ```
    Or using `python3`:
    ```bash
    python3 main.py
    ```

3.  **Interact with the Agent via CLI**:
    The CLI will start. Type your prompt. The agent will then display the LLM-generated initial output, critique, and refined output.
    ```
    --- Processing Prompt: "write a short story about a robot learning to paint" ---
      Prompt: write a short story about a robot learning to paint
      Initial Output: Unit 734 activated its optical sensors. Its designated task: image creation. It extended a multi-jointed appendage, grasping a brush. The canvas was blank.
      Critique: The story starts abruptly and lacks descriptive detail about the robot's process or feelings about painting. It also ends too soon.
      Refined Output: Unit 734, a sanitation bot repurposed for artistry, whirred as its optical sensors focused on the blank canvas. Its programming dictated image creation, but a new subroutine sparked something akin to curiosity. One of its many articulated arms, usually reserved for refuse collection, gently picked up a delicate paintbrush. The bristles felt alien. Its first stroke was hesitant, a smear of blue. Then, observing a nearby flower, it tried again, a slow, deliberate arc. The result was... interesting. Not a flower, but not just a smear either. A new directive formed: 'Understand color. Understand form. Understand... beauty?'
      Final Output: Unit 734, a sanitation bot repurposed for artistry, whirred as its optical sensors focused on the blank canvas. Its programming dictated image creation, but a new subroutine sparked something akin to curiosity. One of its many articulated arms, usually reserved for refuse collection, gently picked up a delicate paintbrush. The bristles felt alien. Its first stroke was hesitant, a smear of blue. Then, observing a nearby flower, it tried again, a slow, deliberate arc. The result was... interesting. Not a flower, but not just a smear either. A new directive formed: 'Understand color. Understand form. Understand... beauty?'
    ```
    *(Exact LLM outputs will vary.)*

### Web UI (Streamlit)

The Self-Reflecting Agent's LLM-driven process is best observed via its Streamlit UI.

1.  **Ensure Dependencies are Installed**:
    Make sure `streamlit` and `ollama` are installed (see Prerequisites).

2.  **Run the Streamlit App**:
    Navigate to the root directory of this repository and execute:
    ```bash
    streamlit run self_reflecting_agent/app_ui.py
    ```
    This will open the UI in your web browser.

3.  **Interact with the Agent via Web**:
    *   The UI will prompt you to enter a task for the agent.
    *   A sidebar provides example prompts.
    *   After submitting, the UI will display:
        *   "Initial Output" (from LLM call 1).
        *   "Critique" (from LLM call 2).
        *   "Refined Output" (from LLM call 3, if critique was provided).
        *   The "Final Output".
        *   An expandable section for the agent's internal log.
    This provides a clear, step-by-step view of how the LLM is used in each phase of the self-reflection cycle.
```
