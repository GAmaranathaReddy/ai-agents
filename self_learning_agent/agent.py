# agent.py
import random
from typing import List, Dict, Tuple

class SelfLearningAgent_RPS:
    def __init__(self, random_choice_threshold: int = 3):
        """
        Initializes the Self-Learning Rock-Paper-Scissors Agent.

        Args:
            random_choice_threshold (int): Number of opponent moves to observe
                                           before trying to predict.
        """
        self.opponent_move_history: List[str] = []
        self.move_counts: Dict[str, int] = {"rock": 0, "paper": 0, "scissors": 0}
        self.possible_moves: List[str] = ["rock", "paper", "scissors"]
        self.random_choice_threshold: int = random_choice_threshold
        self.name: str = "LearnerBot-RPS"

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


if __name__ == '__main__':
    print("Testing SelfLearningAgent_RPS...")
    agent = SelfLearningAgent_RPS(random_choice_threshold=2)

    print(f"Initial choice (random): {agent.choose_action()}")

    agent.learn("rock")
    print(f"Learned 'rock'. History: {agent.opponent_move_history}, Counts: {agent.move_counts}")
    print(f"Choice after 1 'rock' (random): {agent.choose_action()}") # Still random

    agent.learn("rock")
    print(f"Learned 'rock' again. History: {agent.opponent_move_history}, Counts: {agent.move_counts}")
    # Now history length is 2, so it should predict based on 'rock' (most frequent)
    # Predicts opponent plays 'rock', agent should play 'paper'
    print(f"Choice after 2 'rock' (should be 'paper'): {agent.choose_action()}")

    agent.learn("paper")
    print(f"Learned 'paper'. History: {agent.opponent_move_history}, Counts: {agent.move_counts}")
    # Opponent moves: rock (2), paper (1). Predicts 'rock', agent plays 'paper'.
    print(f"Choice (should be 'paper'): {agent.choose_action()}")

    agent.learn("scissors")
    agent.learn("scissors")
    agent.learn("scissors")
    print(f"Learned 'scissors' x3. History: {agent.opponent_move_history}, Counts: {agent.move_counts}")
    # Opponent moves: rock (2), paper (1), scissors (3). Predicts 'scissors', agent plays 'rock'.
    print(f"Choice (should be 'rock'): {agent.choose_action()}")

    agent.reset_memory()
    print(f"After reset: History: {agent.opponent_move_history}, Counts: {agent.move_counts}")
    print(f"Choice after reset (random): {agent.choose_action()}")
