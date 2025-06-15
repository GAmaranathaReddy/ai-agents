# main.py
from agent import ReActRAGAgent

def main():
    """
    Main function to run the CLI for interacting with the ReAct-RAG Agent.
    """
    print("ReAct-RAG Agent CLI")
    print("Ask about topics like Python, Java, AI, ReAct, or RAG.")
    print("Try phrases like 'tell me about python', 'what is ai?', 'explain rag'.")
    print("Type 'exit' or 'quit' to stop.")
    print("-" * 30)

    agent = ReActRAGAgent()

    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() in ['exit', 'quit']:
                print("Exiting agent CLI. Goodbye!")
                break

            if not user_input.strip():
                print("Agent: Please say something or ask a question.")
                continue

            agent_response = agent.reason_and_act(user_input)
            # The agent.py can be configured to return thoughts for debugging.
            # For this CLI, we'll just show the final response.
            print(f"Agent: {agent_response}")

        except EOFError:
            print("\nExiting agent CLI. Goodbye!")
            break
        except KeyboardInterrupt:
            print("\nExiting agent CLI. Goodbye!")
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            # break # Uncomment if you want to exit on any error

if __name__ == "__main__":
    main()
