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
    st.title("🏡 Environment-Controlled Agent Simulation (LLM-Powered)")
    st.markdown(f"Watch `{st.session_state.eco_agent.name}` interact with its environment based on natural language goals.")

    # Sidebar for Goal Setting and Info
    st.sidebar.header("Agent Control & Info")
    new_goal_input = st.sidebar.text_area(
        "Set a new goal for the agent:",
        value=st.session_state.eco_agent.current_goal, # Show current goal
        height=100,
        key="new_goal_text_area"
    )
    if st.sidebar.button("Update Goal", key="update_goal_button"):
        confirmation = st.session_state.eco_agent.set_goal(new_goal_input)
        st.sidebar.success(confirmation)
        # Add goal change to log for clarity
        log_entry_goal_change = {
            "step": "GOAL UPDATE",
            "timestamp": datetime.datetime.now().strftime("%H:%M:%S"),
            "new_goal": new_goal_input,
            "confirmation": confirmation
        }
        st.session_state.action_log.insert(0, log_entry_goal_change)
        st.experimental_rerun()

    st.sidebar.markdown("---")
    st.sidebar.subheader("Current Agent Goal:")
    st.sidebar.info(st.session_state.eco_agent.current_goal)
    st.sidebar.markdown("---")
    st.sidebar.subheader("Agent's Decision Logic:")
    st.sidebar.markdown(
        "The agent uses an LLM (Ollama) to interpret its current goal against the environment state "
        "and decide which action (toggle light, set temperature, or do nothing) is best, along with an explanation."
    )
    st.sidebar.markdown("---")
    st.sidebar.subheader("Environment Details:")
    st.sidebar.markdown("""
    - `light_on`: boolean (True/False)
    - `temperature`: integer (°C)
    """)


    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("Environment State")
        current_env_state = st.session_state.environment.get_state()
        st.json(current_env_state)

        if st.button("Run Next Step", key="run_step_button"):
            st.session_state.step_count += 1
            log_entry = {
                "step": st.session_state.step_count,
                "timestamp": datetime.datetime.now().strftime("%H:%M:%S"),
                "goal_at_step": st.session_state.eco_agent.current_goal # Log current goal
            }

            # 1. Agent perceives
            perceived_state = st.session_state.eco_agent.perceive()
            log_entry["perceived_state"] = perceived_state

            # 2. Agent decides (now returns explanation too)
            action_to_take, action_value, explanation = st.session_state.eco_agent.decide_action(perceived_state)
            log_entry["decided_action"] = action_to_take
            log_entry["action_value"] = action_value
            log_entry["explanation"] = explanation # Store explanation

            # 3. Agent executes
            execution_result = st.session_state.eco_agent.execute_action(action_to_take, action_value)
            log_entry["execution_result"] = execution_result

            # Log the new state after action
            log_entry["new_env_state"] = st.session_state.environment.get_state()

            st.session_state.action_log.insert(0, log_entry) # Add to top for reverse chronological display
            st.experimental_rerun() # Rerun to update the displayed environment state and log

        if st.button("Reset Simulation", key="reset_sim_button"):
            # Preserve current LLM model, but reset environment, agent (with new env), log, step count
            current_llm_model = st.session_state.eco_agent.llm_model
            st.session_state.environment = Environment()
            st.session_state.eco_agent = EnvironmentControlledAgent(st.session_state.environment, llm_model=current_llm_model)
            # Goal resets to default in agent's __init__
            st.session_state.action_log = []
            st.session_state.step_count = 0
            st.sidebar.success("Simulation and agent goal reset to default.") # Feedback
            st.experimental_rerun()


    with col2:
        st.subheader("Simulation Log (Newest First)")
        if not st.session_state.action_log:
            st.info("Click 'Run Next Step' to start the simulation or 'Update Goal' to set a new goal.")
        else:
            for i, entry in enumerate(st.session_state.action_log):
                if "new_goal" in entry: # Log entry for goal change
                    with st.expander(f"Goal Update ({entry['timestamp']})", expanded=True):
                        st.success(entry['confirmation'])
                else: # Log entry for simulation step
                    exp_title = f"Step {entry['step']} ({entry['timestamp']}) - Action: {entry['decided_action']}"
                    with st.expander(exp_title, expanded=(i==0)): # Expand newest entry
                        st.markdown(f"**Goal:** _{entry.get('goal_at_step', 'N/A')}_")
                        st.markdown(f"**Agent Perceived:** `{entry['perceived_state']}`")
                        action_display = f"`{entry['decided_action']}`"
                        if entry['action_value'] is not None:
                            action_display += f" with value `{entry['action_value']}`"
                        st.markdown(f"**Agent Decided:** {action_display}")
                        st.markdown(f"**LLM Reasoning:** \"{entry.get('explanation', 'N/A')}\"")
                        st.markdown(f"**Execution Result:** `{entry['execution_result']}`")
                        st.markdown(f"**New Environment State:** `{entry['new_env_state']}`")


if __name__ == "__main__":
    main()
