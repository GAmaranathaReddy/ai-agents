# Self-Reflecting Agent

## Self-Reflecting Agent (LLM-Powered via Abstraction Layer)

A Self-Reflecting Agent improves its output through a cycle of generation, evaluation (critique), and refinement. This version is **fully LLM-powered**, using the **common LLM provider abstraction layer** (which can be Ollama, OpenAI, Gemini, or Bedrock based on global configuration) for each stage of this process.

1.  **Generation**: Given a user prompt, the configured LLM provider generates an initial draft.
2.  **Critique**: A second call to the LLM provider evaluates this draft against the original prompt, providing specific feedback for improvement.
3.  **Refinement**: A third call to the LLM provider takes the original draft, the critique, and the initial prompt, and attempts to produce a revised output that addresses the critique.

This cycle aims to produce higher-quality, more nuanced results.

## Implementation

This project demonstrates the fully LLM-driven Self-Reflecting Agent pattern using the common LLM provider abstraction:

1.  **`task_performer.py` (Updated)**:
    *   `generate_initial_output(prompt: str, llm_provider: BaseLLMProvider)`: Calls `llm_provider.chat()` with the user `prompt` to produce a first draft.
    *   `refine_output(initial_output: str, critique: str, original_prompt: str, llm_provider: BaseLLMProvider)`: Constructs a prompt for the `llm_provider` incorporating the initial output, critique, and original prompt, instructing it to generate a revised version.

2.  **`critique_mechanism.py` (Updated)**:
    *   `critique_output(output_to_critique: str, original_prompt: str, llm_provider: BaseLLMProvider)`: Uses the `llm_provider.chat()` to evaluate the `output_to_critique` based on the `original_prompt`, guided by a specific critique-generation prompt. Normalizes "no critique" LLM responses.

3.  **`agent.py` (`SelfReflectingAgent` class - Updated)**:
    *   No longer directly manages LLM model names. In `__init__`, it calls `get_llm_provider_instance()` from `common.llm_config` to get the globally configured LLM provider.
    *   The `process_request(user_prompt: str)` method orchestrates the self-reflection loop, passing the `self.llm_provider` instance to `generate_initial_output`, `critique_output`, and `refine_output`.
    *   Logs interactions and returns a structured dictionary with all stages of the process.

4.  **`main.py` (CLI)** and **`app_ui.py` (Streamlit UI)**:
    *   Interact with the refactored `SelfReflectingAgent`. The UI visualizes the LLM-generated outputs for each stage.

## Prerequisites & Setup

1.  **LLM Provider Configuration**:
    *   This agent uses the centrally configured LLM provider. Ensure you have set up your desired LLM provider (Ollama, OpenAI, Gemini, or AWS Bedrock) and configured the necessary environment variables (e.g., `LLM_PROVIDER`, `OLLAMA_MODEL`, `OPENAI_API_KEY`, etc.).
    *   **Refer to the "Multi-LLM Provider Support" section in the main project README** for detailed instructions on setting up environment variables and installing provider-specific SDKs. A model good at instruction-following is recommended for all stages of this agent (generation, critique, and refinement).

2.  **Streamlit (for UI)**:
    *   Install Streamlit (listed in this agent's `requirements.txt`):
      ```bash
      pip install streamlit
      ```

*(If using Poetry for the main project, ensure `streamlit` and the chosen LLM provider's SDK are added to your `pyproject.toml`.)*

## How to Run

**(Ensure you have completed all Prerequisites & Setup steps above: chosen LLM provider configured, its service running if needed, and Python packages installed.)**

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
