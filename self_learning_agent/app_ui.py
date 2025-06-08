import streamlit as st
from agent import SelfLearningAgent_RPS
from game import determine_winner

# Initialize agent, scores, and last round info in session state
if 'rps_agent' not in st.session_state:
    st.session_state.rps_agent = SelfLearningAgent_RPS(random_choice_threshold=3)

if 'player_score' not in st.session_state:
    st.session_state.player_score = 0
if 'agent_score' not in st.session_state:
    st.session_state.agent_score = 0
if 'ties' not in st.session_state:
    st.session_state.ties = 0

if 'last_player_move' not in st.session_state:
    st.session_state.last_player_move = None
if 'last_agent_move' not in st.session_state:
    st.session_state.last_agent_move = None
if 'last_winner' not in st.session_state:
    st.session_state.last_winner = None

if 'game_round' not in st.session_state:
    st.session_state.game_round = 0


def play_round(player_choice: str):
    st.session_state.game_round += 1
    agent = st.session_state.rps_agent

    # 1. Agent chooses action
    agent_choice = agent.choose_action()
    st.session_state.last_agent_move = agent_choice
    st.session_state.last_player_move = player_choice

    # 2. Determine winner
    winner = determine_winner(agent_choice, player_choice)
    st.session_state.last_winner = winner

    # 3. Update scores
    if winner == "player":
        st.session_state.player_score += 1
    elif winner == "agent":
        st.session_state.agent_score += 1
    else:
        st.session_state.ties += 1

    # 4. Agent learns
    agent.learn(player_choice)

def reset_game():
    st.session_state.rps_agent.reset_memory()
    st.session_state.player_score = 0
    st.session_state.agent_score = 0
    st.session_state.ties = 0
    st.session_state.last_player_move = None
    st.session_state.last_agent_move = None
    st.session_state.last_winner = None
    st.session_state.game_round = 0


def main():
    st.set_page_config(page_title="RPS Self-Learning Agent", layout="centered")
    st.title("🤖 Self-Learning Agent: Rock-Paper-Scissors")

    st.markdown(f"Playing against: **{st.session_state.rps_agent.name}**")
    st.markdown(f"Agent starts predicting after **{st.session_state.rps_agent.random_choice_threshold}** of your moves.")
    st.markdown("---")

    # Player move selection
    st.subheader("Choose your move:")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🪨 Rock", use_container_width=True):
            play_round("rock")
    with col2:
        if st.button("📄 Paper", use_container_width=True):
            play_round("paper")
    with col3:
        if st.button("✂️ Scissors", use_container_width=True):
            play_round("scissors")

    st.markdown("---")

    # Display last round's results
    if st.session_state.last_player_move:
        st.subheader(f"Round {st.session_state.game_round} Results:")
        st.markdown(f"You played: **{st.session_state.last_player_move.capitalize()}**")
        st.markdown(f"Agent played: **{st.session_state.last_agent_move.capitalize()}**")

        if st.session_state.last_winner == "player":
            st.success("🎉 You won this round!")
        elif st.session_state.last_winner == "agent":
            st.error("🤖 Agent won this round!")
        else:
            st.warning("🤝 It's a tie!")
        st.markdown("---")

    # Display scores
    st.subheader("📊 Overall Scores:")
    score_col1, score_col2, score_col3 = st.columns(3)
    score_col1.metric("Your Wins", st.session_state.player_score)
    score_col2.metric("Agent Wins", st.session_state.agent_score)
    score_col3.metric("Ties", st.session_state.ties)

    st.markdown("---")

    # Agent's learned knowledge
    with st.expander("🧠 View Agent's Learned Knowledge (Opponent Move Counts)"):
        st.bar_chart(st.session_state.rps_agent.move_counts)
        st.write(st.session_state.rps_agent.move_counts)

    # Reset game button
    st.sidebar.header("Game Controls")
    if st.sidebar.button("Reset Game and Agent Memory"):
        reset_game()
        st.experimental_rerun() # Rerun to reflect reset state immediately

    st.sidebar.header("About")
    st.sidebar.info(
        "This agent learns your Rock-Paper-Scissors move patterns over time. "
        "Initially, it plays randomly. After observing a few of your moves, "
        "it tries to predict your next move based on frequency and play the counter move."
    )

if __name__ == "__main__":
    main()
