# main.py
from agent import SelfLearningAgent_RPS
from game import determine_winner

def print_scores(scores: dict, agent_name: str):
    """Prints the current scores."""
    print(f"Scores: Player - {scores['player']}, {agent_name} - {scores['agent']}, Ties - {scores['tie']}")

def main_game_loop():
    """
    Main loop for the Rock-Paper-Scissors game.
    """
    agent = SelfLearningAgent_RPS(random_choice_threshold=3) # Agent starts predicting after 3 user moves
    rounds_to_play = 10
    scores = {"player": 0, "agent": 0, "tie": 0}
    possible_moves = ["rock", "paper", "scissors"]

    print("--- Welcome to Rock-Paper-Scissors against the Self-Learning Agent! ---")
    print(f"You will play {rounds_to_play} rounds against {agent.name}.")
    print("The agent will try to learn your patterns.")
    print("Type 'rock', 'paper', or 'scissors'. Type 'exit' or 'quit' to end early.")
    print("-" * 30)

    for round_num in range(1, rounds_to_play + 1):
        print(f"\n--- Round {round_num}/{rounds_to_play} ---")
        print_scores(scores, agent.name)

        # 1. Agent chooses an action
        agent_move = agent.choose_action()

        # 2. Prompt user for their move
        player_move = ""
        while player_move not in possible_moves:
            player_input = input(f"Your move ({', '.join(possible_moves)}): ").lower().strip()
            if player_input in ['exit', 'quit']:
                print("Exiting game early.")
                return
            if player_input in possible_moves:
                player_move = player_input
            else:
                print(f"Invalid move. Please choose from: {', '.join(possible_moves)}.")

        # 3. Determine the winner
        winner = determine_winner(agent_move, player_move)

        # Print moves and winner
        print(f"  {agent.name} played: {agent_move.capitalize()}")
        print(f"  You played: {player_move.capitalize()}")

        if winner == "agent":
            print("  Result: Agent wins this round!")
            scores["agent"] += 1
        elif winner == "player":
            print("  Result: You win this round!")
            scores["player"] += 1
        else: # tie
            print("  Result: It's a tie!")
            scores["tie"] += 1

        # 4. Call agent's learn method
        agent.learn(player_move)
        # print(f"  (Agent's learned counts: {agent.move_counts})") # Optional: for debugging

        if round_num == rounds_to_play:
            print("\n--- End of Game ---")

    # After the loop, print final scores and agent's learned knowledge
    print("\n--- Final Results ---")
    print_scores(scores, agent.name)

    if scores["player"] > scores["agent"]:
        print("Congratulations! You beat the agent.")
    elif scores["agent"] > scores["player"]:
        print(f"{agent.name} won the game. Better luck next time!")
    else:
        print("The game was a tie overall!")

    print(f"\n{agent.name}'s final learned opponent move counts: {agent.move_counts}")
    # print(f"Opponent move history (last 10): {agent.opponent_move_history[-10:]}") # If history gets too long

if __name__ == "__main__":
    main_game_loop()
