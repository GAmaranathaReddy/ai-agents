# Self-Learning Agent (Rock-Paper-Scissors Example)

## Self-Learning Agent Pattern

A Self-Learning Agent is an agent that improves its performance, decision-making, or knowledge over time by learning from its experiences and interactions. Unlike agents with fixed logic, a self-learning agent adapts its behavior based on feedback, new data, or observed outcomes.

The core components of this pattern usually involve:

1.  **Experience/Data Collection**: The agent gathers data from its interactions or environment. This could be user inputs, game outcomes, sensor readings, etc.
2.  **Knowledge Representation/Memory**: The agent has a way to store and organize the information it learns. This might be a simple frequency count, a more complex model, a set of rules, or a neural network.
3.  **Learning Mechanism**: A process by which the agent updates its internal knowledge or model based on new experiences. This is where the "learning" happens.
4.  **Action Strategy**: The agent uses its current knowledge to make decisions or choose actions, intending to perform better as its knowledge grows.

The goal is for the agent to become more effective, efficient, or accurate as it gains more experience.

## Implementation (Rock-Paper-Scissors Example)

This project demonstrates a simple self-learning agent that plays Rock-Paper-Scissors (RPS) against a human player. The agent tries to learn the player's move patterns to improve its chances of winning.

1.  **`agent.py`**:
    *   Defines the `SelfLearningAgent_RPS` class.
    *   **Knowledge Representation/Memory**:
        *   `opponent_move_history` (list): Stores a chronological list of all valid moves made by the human player.
        *   `move_counts` (dictionary): Keeps track of the frequency of each move the opponent has made (e.g., `{"rock": 5, "paper": 3, "scissors": 2}`).
    *   **`learn(opponent_last_move: str)` method (Learning Mechanism)**:
        *   This method is called after each round.
        *   It takes the `opponent_last_move` (the human player's move for that round) as input.
        *   It appends this move to `opponent_move_history`.
        *   It increments the count for `opponent_last_move` in the `move_counts` dictionary. This is how the agent updates its understanding of the opponent's tendencies.
    *   **`choose_action()` method (Action Strategy)**:
        *   This method decides the agent's next move (rock, paper, or scissors).
        *   **Initial Phase**: If the `opponent_move_history` is short (e.g., fewer than 3 moves, defined by `random_choice_threshold`), the agent doesn't have enough data to make an informed prediction, so it chooses a move randomly.
        *   **Learning Phase**: Once enough data is collected, the agent attempts to predict the opponent's next move by looking at `move_counts`. It identifies which of the opponent's moves ("rock", "paper", or "scissors") has been the most frequent so far.
        *   **Counter-Action**: After predicting the opponent's likely move, the agent chooses the action that would beat that predicted move (e.g., if it predicts the opponent will play "rock", the agent plays "paper").
    *   `reset_memory()`: A utility to clear the agent's learned history and counts.

2.  **`game.py`**:
    *   Contains a helper function `determine_winner(agent_move: str, player_move: str)` which takes the agent's and player's moves and returns "agent", "player", or "tie" based on standard RPS rules.

3.  **`main.py`**:
    *   Initializes the `SelfLearningAgent_RPS`.
    *   Manages the game loop for a set number of rounds (e.g., 10).
    *   In each round:
        1.  The agent calls `choose_action()` to select its move.
        2.  The human player is prompted to enter their move (with input validation).
        3.  `determine_winner()` is called to find out the result of the round.
        4.  The outcome is printed, and scores are updated.
        5.  Crucially, the agent's `learn(player_move)` method is called, allowing it to update its knowledge based on the player's actual move.
    *   After all rounds, the final scores and the agent's learned `move_counts` are displayed, showing what patterns the agent picked up on.

This implementation demonstrates a basic form of frequency analysis for learning. As the game progresses, if the player exhibits any habitual patterns (e.g., playing "rock" more often), the agent's `move_counts` will reflect this, and its `choose_action` strategy will increasingly try to counter that pattern.

## How to Run

1.  **Navigate to the project directory**:
    Open your terminal or command prompt.
    ```bash
    cd path/to/your/self_learning_agent
    ```

2.  **Ensure all files are present**:
    You should have `agent.py`, `game.py`, and `main.py` in this directory.

3.  **Run the `main.py` script**:
    ```bash
    python main.py
    ```
    Or, if you have multiple Python versions, you might need to use `python3`:
    ```bash
    python3 main.py
    ```

4.  **Play the Game**:
    *   The script will welcome you and explain the rules.
    *   In each round, it will display current scores and prompt you for your move ("rock", "paper", or "scissors").
    *   After you enter your move, it will show the agent's move, the result of the round, and then proceed to the next round.
    *   The game continues for a predefined number of rounds (default 10).
    *   At the end, it will show the final scores and what the agent "learned" about your move frequencies.

    **Example Interaction Snippet**:
    ```
    --- Welcome to Rock-Paper-Scissors against the Self-Learning Agent! ---
    You will play 10 rounds against LearnerBot-RPS.
    The agent will try to learn your patterns.
    Type 'rock', 'paper', or 'scissors'. Type 'exit' or 'quit' to end early.
    ------------------------------

    --- Round 1/10 ---
    Scores: Player - 0, LearnerBot-RPS - 0, Ties - 0
    Your move (rock, paper, scissors): rock
      LearnerBot-RPS played: Paper
      You played: Rock
      Result: Agent wins this round!

    --- Round 2/10 ---
    Scores: Player - 0, LearnerBot-RPS - 1, Ties - 0
    Your move (rock, paper, scissors): paper
      LearnerBot-RPS played: Rock
      You played: Paper
      Result: You win this round!
    ...
    --- Final Results ---
    Scores: Player - X, LearnerBot-RPS - Y, Ties - Z
    Congratulations! You beat the agent. / LearnerBot-RPS won the game. / The game was a tie overall!

    LearnerBot-RPS's final learned opponent move counts: {'rock': A, 'paper': B, 'scissors': C}
    ```
