from agent import LLMEnhancedAgent

def main():
    """
    Main function to run the CLI for interacting with the LLM-Enhanced Agent.
    """
    print("LLM-Enhanced Agent CLI")
    print("Type 'exit' or 'quit' to stop.")
    print("-" * 30)

    # Initialize the agent
    # You can specify a conceptual LLM service name if you like
    agent = LLMEnhancedAgent(llm_service_name="MyCustomLLM")

    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() in ['exit', 'quit']:
                print("Exiting agent CLI. Goodbye!")
                break

            if not user_input:
                print("Agent: Please say something.")
                continue

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
