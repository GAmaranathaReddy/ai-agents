# main.py
from agent import ToolEnhancedAgent

def main():
    """
    Main function to run the CLI for interacting with the Tool-Enhanced Agent.
    """
    print("Tool-Enhanced Agent CLI")
    print(f"Powered by: {ToolEnhancedAgent().name}")
    print("You can ask for the current time/date, calculate sums (e.g., 'add 10 and 5'),")
    print("or get the weather (e.g., 'what's the weather in London?').")
    print("Type 'exit' or 'quit' to stop.")
    print("-" * 30)

    agent = ToolEnhancedAgent()

    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() in ['exit', 'quit']:
                print("Exiting agent CLI. Goodbye!")
                break

            if not user_input.strip():
                print("Agent: Please type a command or question.")
                continue

            agent_response = agent.process_request(user_input)
            print(f"Agent: {agent_response}")

        except EOFError:
            print("\nExiting agent CLI. Goodbye!")
            break
        except KeyboardInterrupt:
            print("\nExiting agent CLI. Goodbye!")
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            # Depending on severity, you might want to:
            # break

if __name__ == "__main__":
    main()
