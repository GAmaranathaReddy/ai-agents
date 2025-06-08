from automation import FixedAutomationAgent

def main():
    """
    Main function to run the CLI for interacting with the Fixed Automation Agent.
    """
    print("Fixed Automation Agent CLI")
    print(f"Powered by: RuleBot V1")
    print("Type 'exit' or 'quit' to stop.")
    print("Example commands: 'hello', 'about', 'add X Y', 'multiply X Y'")
    print("-" * 30)

    # Initialize the agent
    agent = FixedAutomationAgent()

    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() in ['exit', 'quit']:
                print("Exiting agent CLI. Goodbye!")
                break

            if not user_input:
                # Agent doesn't have a specific response for empty input in its rules,
                # so it will fall to the default "don't understand" message.
                # Or we can handle it here:
                # print("Agent: Please enter a command.")
                # continue
                pass # Let the agent handle it

            agent_response = agent.process_request(user_input)
            print(f"Agent: {agent_response}")

        except EOFError:
            # Handle Ctrl+D (EOF) to exit gracefully
            print("\nExiting agent CLI. Goodbye!")
            break
        except KeyboardInterrupt:
            # Handle Ctrl+C to exit gracefully
            print("\nExiting agent CLI. Goodbye!")
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            # Optionally, decide if the error is critical enough to exit
            # break

if __name__ == "__main__":
    main()
