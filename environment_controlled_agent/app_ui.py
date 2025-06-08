import streamlit as st
from agent import EnvironmentControlledAgent
from environment import Environment
import datetime

# Initialize environment, agent, and log in session state
if 'environment' not in st.session_state:
    st.session_state.environment = Environment()
    # Optionally set a more dynamic initial state for demo variability
    # st.session_state.environment.states["temperature"] = random.randint(10, 30)
    # st.session_state.environment.states["light_on"] = random.choice([True, False])

if 'eco_agent' not in st.session_state:
    st.session_state.eco_agent = EnvironmentControlledAgent(st.session_state.environment)

if 'action_log' not in st.session_state:
    st.session_state.action_log = [] # Stores log messages for each step

if 'step_count' not in st.session_state:
    st.session_state.step_count = 0


def main():
    st.set_page_config(page_title="Environment-Controlled Agent Sim", layout="wide")
    st.title("🏡 Environment-Controlled Agent Simulation")
    st.markdown(f"Watch `{st.session_state.eco_agent.name}` interact with its environment.")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("Environment State")
        current_env_state = st.session_state.environment.get_state()
        st.json(current_env_state)

        if st.button("Run Next Step", key="run_step_button"):
            st.session_state.step_count += 1
            log_entry = {"step": st.session_state.step_count, "timestamp": datetime.datetime.now().strftime("%H:%M:%S")}

            # 1. Agent perceives
            perceived_state = st.session_state.eco_agent.perceive()
            log_entry["perceived_state"] = perceived_state

            # 2. Agent decides
            action_to_take, action_value = st.session_state.eco_agent.decide_action(perceived_state)
            log_entry["decided_action"] = action_to_take
            log_entry["action_value"] = action_value

            # 3. Agent executes
            execution_result = st.session_state.eco_agent.execute_action(action_to_take, action_value)
            log_entry["execution_result"] = execution_result

            # Log the new state after action
            log_entry["new_env_state"] = st.session_state.environment.get_state()

            st.session_state.action_log.insert(0, log_entry) # Add to top for reverse chronological display
            st.experimental_rerun() # Rerun to update the displayed environment state and log

        if st.button("Reset Simulation", key="reset_sim_button"):
            st.session_state.environment = Environment()
            st.session_state.eco_agent = EnvironmentControlledAgent(st.session_state.environment)
            st.session_state.action_log = []
            st.session_state.step_count = 0
            st.experimental_rerun()


    with col2:
        st.subheader("Simulation Log (Newest First)")
        if not st.session_state.action_log:
            st.info("Click 'Run Next Step' to start the simulation.")
        else:
            for i, entry in enumerate(st.session_state.action_log):
                with st.expander(f"Step {entry['step']} ({entry['timestamp']}) - Action: {entry['decided_action']}", expanded=(i==0)):
                    st.markdown(f"**Agent Perceived:** `{entry['perceived_state']}`")
                    action_display = f"`{entry['decided_action']}`"
                    if entry['action_value'] is not None:
                        action_display += f" with value `{entry['action_value']}`"
                    st.markdown(f"**Agent Decided:** {action_display}")
                    st.markdown(f"**Execution Result:** `{entry['execution_result']}`")
                    st.markdown(f"**New Environment State:** `{entry['new_env_state']}`")

    # Sidebar for information
    st.sidebar.header("About This Simulation")
    st.sidebar.info(
        f"The agent, '{st.session_state.eco_agent.name}', observes the environment and tries to maintain optimal conditions."
    )
    st.sidebar.markdown("---")
    st.sidebar.subheader("Agent's Goals:")
    st.sidebar.markdown("""
    - Keep the light ON if it's OFF.
    - Keep the temperature between 18°C and 25°C.
      - If temperature < 18°C, set to 22°C.
      - If temperature > 25°C, set to 22°C.
    """)
    st.sidebar.markdown("---")
    st.sidebar.subheader("Environment Details:")
    st.sidebar.markdown("""
    - `light_on`: boolean (True/False)
    - `temperature`: integer (°C)
    """)

if __name__ == "__main__":
    main()
