# game.py
from typing import Literal

def determine_winner(agent_move: str, player_move: str) -> Literal["agent", "player", "tie"]:
    """
    Determines the winner of a Rock-Paper-Scissors round.

    Args:
        agent_move (str): The agent's move ("rock", "paper", or "scissors").
        player_move (str): The player's move ("rock", "paper", or "scissors").

    Returns:
        Literal["agent", "player", "tie"]: The winner of the round.
                                           Returns "tie" if moves are invalid or the same.
    """
    valid_moves = ["rock", "paper", "scissors"]
    agent_move = agent_move.lower()
    player_move = player_move.lower()

    if agent_move not in valid_moves or player_move not in valid_moves:
        # This case should ideally be caught by input validation before calling this function,
        # but as a safeguard:
        return "tie" # Or raise an error, or handle as an invalid round

    if agent_move == player_move:
        return "tie"

    winning_combinations = {
        ("rock", "scissors"),  # Agent's rock beats player's scissors
        ("paper", "rock"),     # Agent's paper beats player's rock
        ("scissors", "paper")  # Agent's scissors beats player's paper
    }

    if (agent_move, player_move) in winning_combinations:
        return "agent"
    else:
        # If it's not a tie and the agent didn't win, the player must have won.
        return "player"

if __name__ == '__main__':
    print("Testing determine_winner function...")
    test_cases = [
        ("rock", "scissors", "agent"),
        ("paper", "rock", "agent"),
        ("scissors", "paper", "agent"),
        ("rock", "paper", "player"),
        ("paper", "scissors", "player"),
        ("scissors", "rock", "player"),
        ("rock", "rock", "tie"),
        ("paper", "paper", "tie"),
        ("scissors", "scissors", "tie"),
        ("rock", "invalid_move", "tie") # Example of invalid move handling
    ]

    for agent_m, player_m, expected_winner in test_cases:
        winner = determine_winner(agent_m, player_m)
        print(f"Agent: {agent_m}, Player: {player_m} -> Winner: {winner} (Expected: {expected_winner}) -> {'Correct' if winner == expected_winner else 'Incorrect'}")

    # Test with mixed case inputs
    print("\nTesting with mixed case:")
    winner_mixed = determine_winner("Rock", "scissors")
    print(f"Agent: Rock, Player: scissors -> Winner: {winner_mixed} (Expected: agent) -> {'Correct' if winner_mixed == 'agent' else 'Incorrect'}")
