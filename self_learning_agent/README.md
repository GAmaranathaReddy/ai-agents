# Self-Learning Agent (Rock-Paper-Scissors Example)

## Self-Learning Agent (Rock-Paper-Scissors with LLM Analysis)

A Self-Learning Agent improves its performance or knowledge over time by learning from experiences. This Rock-Paper-Scissors (RPS) agent demonstrates two aspects:
1.  **Basic Frequency-Based Learning**: It learns the opponent's (human player's) move tendencies and tries to play a counter-move.
2.  **LLM-Powered Analysis**: It uses an Ollama LLM to provide a natural language analysis of the opponent's play style after a sufficient number of moves.

The core components:
*   **Experience Collection**: Records the player's move history.
*   **Knowledge Representation**: Stores frequency counts of player's moves (`move_counts`).
*   **Learning Mechanism**: Updates `move_counts` after each round.
*   **Action Strategy**: Chooses randomly initially, then uses `move_counts` to predict and counter the player's most frequent move.
*   **LLM Analysis**: Uses an LLM to analyze the sequence of player moves and describe potential patterns.

## Implementation

1.  **`agent.py` (`SelfLearningAgent_RPS` class - Updated)**:
    *   Initialized with an Ollama `llm_model` (e.g., "mistral") for the analysis feature.
    *   **Frequency-Based Learning**:
        *   `opponent_move_history` (list): Stores the player's moves.
        *   `move_counts` (dictionary): Tracks frequency of "rock", "paper", "scissors".
        *   `learn(opponent_last_move: str)`: Updates history and counts.
        *   `choose_action()`: Plays randomly if history is short; otherwise, predicts player's most frequent move and plays the counter.
    *   **LLM-Powered Analysis (New)**:
        *   `get_llm_analysis_of_opponent()`:
            *   Checks if enough moves (`min_history_for_analysis`) have been played.
            *   Formats the `opponent_move_history` into a string.
            *   Constructs a prompt asking the Ollama LLM to act as a game strategy analyst and describe observable patterns or tendencies in the opponent's moves.
            *   Calls `ollama.chat()` to get the analysis.
            *   Returns the LLM's textual analysis or an error message.
    *   `reset_memory()`: Clears history and counts.

2.  **`game.py`**:
    *   `determine_winner(agent_move: str, player_move: str)`: Standard RPS win/loss/tie logic.

3.  **`main.py` (CLI)**:
    *   Manages the RPS game loop against the agent.
    *   Calls `agent.learn()` after each round.
    *   Displays scores and final learned `move_counts`. (Does not currently use the LLM analysis feature).

4.  **`app_ui.py` (Streamlit UI - Updated)**:
    *   Provides an interactive web interface for playing RPS.
    *   Displays game state, scores, and the agent's learned `move_counts` (frequency analysis).
    *   **New Feature**: Includes a button "🕵️ Get LLM Analysis of Your Play Style". When clicked, it calls `agent.get_llm_analysis_of_opponent()` and displays the LLM's textual analysis of the player's moves.

## Prerequisites & Setup

1.  **Ollama and LLM Model (for Analysis Feature)**:
    *   **Install Ollama**: Ensure Ollama is installed and running. See [Ollama official website](https://ollama.com/).
    *   **Pull an LLM Model**: The agent defaults to `"mistral"` for analysis.
      ```bash
      ollama pull mistral
      ```
    *   **Install Ollama Python Client**:
      ```bash
      pip install ollama
      ```

2.  **Streamlit (for UI)**:
    *   Install Streamlit:
      ```bash
      pip install streamlit
      ```

*(If using Poetry for the main project, add `ollama` and `streamlit` to your `pyproject.toml` and run `poetry install`.)*

## How to Run

**(Ensure Ollama is running and the required model is pulled if you intend to use the LLM analysis feature in the UI.)**

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
