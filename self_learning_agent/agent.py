# agent.py
import random
from typing import List, Dict, Tuple
import ollama

class SelfLearningAgent_RPS:
    def __init__(self, random_choice_threshold: int = 3, llm_model: str = "mistral"):
        """
        Initializes the Self-Learning Rock-Paper-Scissors Agent.

        Args:
            random_choice_threshold (int): Number of opponent moves to observe
                                           before trying to predict based on frequency.
            llm_model (str): The Ollama model to use for play style analysis.
        """
        self.opponent_move_history: List[str] = []
        self.move_counts: Dict[str, int] = {"rock": 0, "paper": 0, "scissors": 0}
        self.possible_moves: List[str] = ["rock", "paper", "scissors"]
        self.random_choice_threshold: int = random_choice_threshold
        self.name: str = "LearnerBot-RPS (with LLM Analyst)"
        self.llm_model = llm_model

    def choose_action(self) -> str:
        """
        Chooses an action (rock, paper, or scissors).
        - If opponent history is short, chooses randomly.
        - Otherwise, predicts opponent's next move based on frequency and plays the counter.
        """
        if len(self.opponent_move_history) < self.random_choice_threshold:
            # Not enough data, choose randomly
            return random.choice(self.possible_moves)
        else:
            # Predict opponent's next move
            # Find the move with the highest count.
            # If there's a tie in counts, it will pick one (behavior depends on dict iteration order or max specifics)
            # For a more robust tie-breaking, one might sort or pick randomly among ties.

            most_frequent_opponent_move = None
            max_count = -1

            # Ensure consistent tie-breaking by checking in a fixed order if counts are equal
            # or by explicitly randomizing among ties. Here, simple max is used.
            # sorted_moves = sorted(self.move_counts.items(), key=lambda item: item[1], reverse=True)
            # most_frequent_opponent_move = sorted_moves[0][0]

            # Simpler way to get the most frequent, though tie-breaking is implicit
            if not self.move_counts: # Should not happen if history >= threshold
                 return random.choice(self.possible_moves)

            most_frequent_opponent_move = max(self.move_counts, key=self.move_counts.get)

            # If all counts are zero (e.g., after a reset or if only invalid moves were learned)
            if self.move_counts[most_frequent_opponent_move] == 0:
                return random.choice(self.possible_moves)

            # Choose the action that beats the predicted opponent move
            if most_frequent_opponent_move == "rock":
                return "paper"
            elif most_frequent_opponent_move == "paper":
                return "scissors"
            elif most_frequent_opponent_move == "scissors":
                return "rock"
            else: # Should not happen with valid moves
                return random.choice(self.possible_moves)

    def learn(self, opponent_last_move: str) -> None:
        """
        Updates the agent's knowledge based on the opponent's last move.

        Args:
            opponent_last_move (str): The opponent's move ("rock", "paper", or "scissors").
        """
        if opponent_last_move not in self.possible_moves:
            # Optionally handle invalid moves, e.g., log an error or ignore
            # print(f"[Agent DEBUG] Invalid move '{opponent_last_move}' received. Not learning.")
            return

        self.opponent_move_history.append(opponent_last_move)
        self.move_counts[opponent_last_move] += 1
        # print(f"[Agent DEBUG] Learned: Opponent played {opponent_last_move}. Counts: {self.move_counts}") # For debugging

    def reset_memory(self) -> None:
        """Resets the agent's learning history and move counts."""
        self.opponent_move_history = []
        self.move_counts = {"rock": 0, "paper": 0, "scissors": 0}
        # print("[Agent DEBUG] Memory reset.")

    def get_llm_analysis_of_opponent(self, min_history_for_analysis: int = 7) -> str:
        """
        Uses an LLM to provide an analysis of the opponent's play style based on history.
        """
        if len(self.opponent_move_history) < min_history_for_analysis:
            return f"Not enough game history for a meaningful analysis. Need at least {min_history_for_analysis} moves. Current moves: {len(self.opponent_move_history)}."

        history_string = ", ".join(self.opponent_move_history)

        prompt_to_llm = (
            "You are a game strategy analyst. Based on the following sequence of moves made by an "
            "opponent in Rock-Paper-Scissors, can you describe any observable patterns, tendencies, "
            "or simple strategies they might be using? Keep your analysis concise (2-3 sentences). "
            f"Opponent's moves: {history_string}"
        )

        try:
            response = ollama.chat(
                model=self.llm_model,
                messages=[{'role': 'user', 'content': prompt_to_llm}]
            )
            analysis = response['message']['content']
            return analysis
        except Exception as e:
            # print(f"[ERROR agent.get_llm_analysis] Ollama error: {e}")
            return f"LLM analysis error: {type(e).__name__}. Is Ollama running and model '{self.llm_model}' pulled?"


if __name__ == '__main__':
    print("Testing SelfLearningAgent_RPS...")
    agent = SelfLearningAgent_RPS(random_choice_threshold=2, llm_model="mistral") # Specify model for test

    print(f"Initial choice (random): {agent.choose_action()}")

    agent.learn("rock")
    print(f"Learned 'rock'. History: {agent.opponent_move_history}, Counts: {agent.move_counts}")
    print(f"Choice after 1 'rock' (random): {agent.choose_action()}")

    agent.learn("rock")
    print(f"Learned 'rock' again. History: {agent.opponent_move_history}, Counts: {agent.move_counts}")
    print(f"Choice after 2 'rock' (should be 'paper' due to freq prediction): {agent.choose_action()}")

    agent.learn("paper")
    print(f"Learned 'paper'. History: {agent.opponent_move_history}, Counts: {agent.move_counts}")
    print(f"Choice (opponent played rock twice, paper once; agent predicts rock, plays paper): {agent.choose_action()}")

    # Test LLM Analysis part
    print("\n--- Testing LLM Analysis ---")
    print("1. Analysis with insufficient history:")
    print(agent.get_llm_analysis_of_opponent(min_history_for_analysis=5)) # Current history is 3

    agent.learn("scissors")
    agent.learn("rock") # History: R, R, P, S, R (5 moves)
    print("\n2. Analysis with sufficient history (5 moves):")
    # This requires Ollama to be running and the model 'mistral' to be pulled.
    # Example: ollama pull mistral
    # The output will be from the LLM.
    analysis_result = agent.get_llm_analysis_of_opponent(min_history_for_analysis=5)
    print(f"LLM Analysis:\n{analysis_result}")

    agent.reset_memory()
    print(f"\nAfter reset: History: {agent.opponent_move_history}, Counts: {agent.move_counts}")
    print(f"Choice after reset (random): {agent.choose_action()}")
    print(f"LLM Analysis after reset: {agent.get_llm_analysis_of_opponent()}")
