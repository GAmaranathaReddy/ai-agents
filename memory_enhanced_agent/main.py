# main.py
from agent import MemoryEnhancedAgent

def main():
    """
    Main function to run the CLI for a conversational interaction
    with the Memory-Enhanced Agent.
    """
    agent = MemoryEnhancedAgent()
    print(f"Memory-Enhanced Agent CLI - Chat with {agent.name}")
    print("The agent can remember your name, favorite color, and other details you share.")
    print("Try saying: 'My name is [Your Name]', 'I like [color]', 'My favorite food is [food]'.")
    print("Then ask: 'What is my name?', 'What is my favorite color?'.")
    print("Type 'exit', 'quit', or 'bye' to end the chat.")
    print("Type 'showmemory' to see what the agent remembers (facts and history).")
    print("-" * 30)

    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() in ['exit', 'quit', 'bye']:
                print(f"Agent: Goodbye, {agent.memory.get_fact('name') if agent.memory.get_fact('name') else 'friend'}!")
                break

            if user_input.lower() == 'showmemory':
                print("\n--- Agent's Current Memory ---")
                print("Facts:", agent.memory.get_all_facts())
                history = agent.memory.get_conversation_history()
                print("History:")
                if history:
                    for u, a in history:
                        print(f"  {u}")
                        print(f"  {a}")
                else:
                    print("  (No history logged yet)")
                print("------------------------------\n")
                continue

            if not user_input.strip():
                print("Agent: Please say something.")
                continue

            agent_response = agent.chat(user_input)
            print(f"Agent: {agent_response}")

        except EOFError:
            print(f"\nAgent: Goodbye, {agent.memory.get_fact('name') if agent.memory.get_fact('name') else 'friend'}!")
            break
        except KeyboardInterrupt:
            print(f"\nAgent: Goodbye, {agent.memory.get_fact('name') if agent.memory.get_fact('name') else 'friend'}!")
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            # break # Depending on severity

if __name__ == "__main__":
    main()
