# Self-Learning Agent (Rock-Paper-Scissors Example)

## Self-Learning Agent (Rock-Paper-Scissors with LLM Analysis via Abstraction Layer)

A Self-Learning Agent improves its performance or knowledge over time by learning from experiences. This Rock-Paper-Scissors (RPS) agent demonstrates:
1.  **Basic Frequency-Based Learning**: It learns the opponent's (human player's) move tendencies and tries to play a counter-move.
2.  **LLM-Powered Analysis**: It uses a **centrally configured LLM provider** (via the common abstraction layer) to provide a natural language analysis of the opponent's play style.

Core components:
*   **Experience Collection**: Records player's move history.
*   **Knowledge Representation**: Stores frequency counts of player's moves (`move_counts`).
*   **Learning Mechanism**: Updates `move_counts`.
*   **Action Strategy (Gameplay)**: Frequency-based prediction and counter-play.
*   **LLM Analysis (Opponent Style)**: Uses the configured LLM provider to analyze move history.

## Implementation

1.  **`agent.py` (`SelfLearningAgent_RPS` class - Updated)**:
    *   No longer directly manages LLM client details or model names for analysis.
    *   In `__init__`, it calls `get_llm_provider_instance()` from `common.llm_config` to get the globally configured LLM provider (Ollama, OpenAI, etc.), which will be used for opponent analysis.
    *   **Frequency-Based Learning** logic (`learn`, `choose_action` based on `move_counts`) remains the same.
    *   **LLM-Powered Analysis (Updated)**:
        *   `get_llm_analysis_of_opponent()`:
            *   Checks for sufficient move history.
            *   Formats history and constructs a prompt for the LLM to analyze opponent tendencies.
            *   Calls `self.llm_provider.chat()` to get the analysis from the configured LLM.
            *   Returns the textual analysis or an error message.
    *   `reset_memory()` is unchanged.

2.  **`game.py`**:
    *   `determine_winner()` logic is unchanged.

3.  **`main.py` (CLI)**:
    *   Focuses on the frequency-based learning gameplay; does not use the LLM analysis feature.

4.  **`app_ui.py` (Streamlit UI - Updated)**:
    *   Provides the interactive RPS game.
    *   Displays scores and agent's learned `move_counts`.
    *   The "🕵️ Get LLM Analysis of Your Play Style" button now triggers the `get_llm_analysis_of_opponent()` method, which uses the abstracted LLM provider.

## Prerequisites & Setup

1.  **LLM Provider Configuration (for Analysis Feature)**:
    *   This agent's analysis feature uses the centrally configured LLM provider. Ensure you have set up your desired LLM provider (Ollama, OpenAI, Gemini, or AWS Bedrock) and configured the necessary environment variables (e.g., `LLM_PROVIDER`, `OLLAMA_MODEL`, `OPENAI_API_KEY`, etc.).
    *   **Refer to the "Multi-LLM Provider Support" section in the main project README** for detailed instructions on setting up environment variables and installing provider-specific SDKs.

2.  **Streamlit (for UI)**:
    *   Install Streamlit (listed in this agent's `requirements.txt`):
      ```bash
      pip install streamlit
      ```

*(If using Poetry for the main project, ensure `streamlit` and the chosen LLM provider's SDK (e.g., `ollama`, `openai`) are added to your `pyproject.toml`.)*

## How to Run

**(Ensure your chosen LLM provider is configured and its service running if needed, especially if you plan to use the LLM analysis feature in the UI.)**

### 1. Command-Line Interface (CLI)

1.  **Navigate to the agent's directory**:
    ```bash
    cd path/to/your/self_learning_agent
    ```

2.  **Run the `main.py` script**:
    ```bash
    python main.py
    ```
    Or using `python3`:
    ```bash
    python3 main.py
    ```
    The CLI version focuses on the frequency-based learning aspect of the agent.

3.  **Play the Game via CLI**:
    Follow on-screen prompts to play Rock-Paper-Scissors. The agent will adapt based on your move frequencies.

### Web UI (Streamlit)

The Streamlit UI provides the full experience, including the LLM-based play style analysis.

1.  **Ensure Dependencies are Installed**:
    Make sure `streamlit` and `ollama` are installed.

2.  **Run the Streamlit App**:
    Navigate to the root directory of this repository and execute:
    ```bash
    streamlit run self_learning_agent/app_ui.py
    ```
    This will open the UI in your web browser.

3.  **Play the Game and Get Analysis via Web**:
    *   Play Rock-Paper-Scissors using the "Rock", "Paper", "Scissors" buttons.
    *   Observe scores and the "Agent's Learned Knowledge" (your move frequencies).
    *   After playing several rounds (e.g., 7-10 moves), click the "🕵️ Get LLM Analysis of Your Play Style" button.
    *   The agent will use Ollama to provide a textual analysis of your move patterns.
    *   Use the "Reset Game and Agent Memory" button in the sidebar to start over.
```
