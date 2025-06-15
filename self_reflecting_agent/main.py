# main.py
from agent import SelfReflectingAgent

def main():
    """
    Main function to run the CLI for interacting with the Self-Reflecting Agent.
    """
    print("Self-Reflecting Agent CLI")
    print(f"Powered by: {SelfReflectingAgent().name}")
    print("Type a prompt for the agent (e.g., 'write a story about a cat', 'plan a trip to Paris').")
    print("Type 'exit' or 'quit' to stop.")
    print("-" * 30)

    agent = SelfReflectingAgent()
    # You can adjust the reflection cycles here if needed, e.g. agent.max_refinement_cycles = 2
    # For this demo, we'll stick to the default of 1 cycle.

    while True:
        try:
            user_prompt = input("You: ")
            if user_prompt.lower() in ['exit', 'quit']:
                print("Exiting agent CLI. Goodbye!")
                break

            if not user_prompt.strip():
                print("Agent: Please enter a prompt.")
                continue

            print("\nAgent is thinking...")
            results = agent.process_request(user_prompt)

            print("\n--- Reflection Process ---")
            print(f"Prompt: \"{results['prompt']}\"")
            print(f"1. Initial Output: \"{results['initial_output']}\"")
            print(f"2. Critique: \"{results['critique']}\"")

            if results['critique'] != "No critique." and results['refined_output']:
                if results['refined_output'] != results['initial_output']:
                    print(f"3. Refined Output: \"{results['refined_output']}\"")
                else:
                    print("3. Refinement Attempted: (Output remained the same after refinement attempt)")
            elif results['critique'] == "No critique.":
                print("3. Refinement: Not needed as there was no critique.")
            else:
                print("3. Refinement: No refined output was generated despite critique.")

            print("--- End of Process ---")
            print(f"Final Agent Output: \"{results['final_output']}\"\n")
            print("-" * 30)


        except EOFError:
            print("\nExiting agent CLI. Goodbye!")
            break
        except KeyboardInterrupt:
            print("\nExiting agent CLI. Goodbye!")
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            # break # Depending on severity

if __name__ == "__main__":
    main()
