# agent.py
# import ollama # No longer directly importing ollama
from common import get_llm_provider_instance # Use the abstraction layer
import json
from memory import Memory
import re # Keep re for simple checks if needed, or remove if LLM handles all parsing

class MemoryEnhancedAgent:
    def __init__(self): # LLM model is now configured via the provider
        self.llm_provider = get_llm_provider_instance()
        self.name = f"RecallBot (using {type(self.llm_provider).__name__})"
        self.memory = Memory()
        # self.llm_model = llm_model # Removed, provider handles its own model config

    # The old _extract_facts and _generate_response methods are removed
    # as their logic is now handled by the LLM.

    def chat(self, user_input: str) -> str:
        """
        Main chat processing method using an LLM for conversation, fact extraction,
        and contextual memory use.
        """
        known_facts = self.memory.get_all_facts()
        # Get last 3 turns (user+agent = 1 turn for LLM context) for context, adjust N as needed
        recent_history_tuples = self.memory.get_last_n_interactions(n=3)

        # Format history for the LLM prompt
        formatted_history = ""
        if recent_history_tuples:
            history_lines = []
            for user_turn, agent_turn in recent_history_tuples:
                history_lines.append(user_turn) # e.g., "user: Hello"
                history_lines.append(agent_turn) # e.g., "agent: Hi there!"
            formatted_history = "\n".join(history_lines)
        else:
            formatted_history = "No recent conversation history."

        # Construct the detailed prompt for Ollama
        prompt_to_llm = f"""You are a helpful and conversational AI assistant named {self.name}.
Your task is to chat with the user, remember facts they tell you, and use those facts in conversation.

Current known facts about the user (in JSON format):
{json.dumps(known_facts if known_facts else {})}

Recent conversation history (last few turns):
<conversation_history>
{formatted_history}
</conversation_history>

User's current message: "{user_input}"

Based on all the above (known facts, history, and current message):
1. Generate a natural, friendly, and relevant conversational "response" to the user's current message. If they ask something you know from facts, use that information.
2. Identify any *new* facts explicitly stated by the user in their *current message* that should be stored or updated in memory. These facts should be key-value pairs. For example, if the user says "My name is Alice", the fact is {{"name": "Alice"}}. If they say "I like blue", it could be {{"likes_color": "blue"}} or {{"favorite_color": "blue"}}. If they say "I live in Paris", it's {{"location": "Paris"}}. If no new facts are explicitly stated, "new_facts_to_store" should be null or an empty dictionary. Do not infer facts not explicitly stated in the *current* message.

Return your output as a single JSON object with two keys: "response" and "new_facts_to_store".
Example:
{{"response": "It's nice to meet you, Bob! I'll remember that you like red.", "new_facts_to_store": {{"name": "Bob", "favorite_color": "red"}}}}
Example if no new facts:
{{"response": "Hi Alice! You mentioned you like blue. What else are you up to today?", "new_facts_to_store": null}}
"""

        agent_reply = f"Sorry, I encountered an issue processing your request: '{user_input}'." # Default error reply
        llm_output_str = "" # For debugging JSON errors

        try:
            # print(f"\n[DEBUG] Prompt to LLM:\n{prompt_to_llm}\n") # For debugging the prompt
            # ollama_response = ollama.chat( # Old call
            #     model=self.llm_model,
            #     messages=[{'role': 'user', 'content': prompt_to_llm}],
            #     format='json' # Request JSON output from Ollama
            # )
            # llm_output_str = ollama_response['message']['content']
            llm_output_str = self.llm_provider.chat(
                messages=[{'role': 'user', 'content': prompt_to_llm}],
                request_json_output=True # Signal to provider to request JSON
            )
            # print(f"[DEBUG] Raw LLM Output: {llm_output_str}") # For debugging
            # Provider should raise error if JSON was requested but not received (for providers that support enforced JSON mode).
            # For others, it's best effort via prompt, so json.loads might fail here.
            llm_data = json.loads(llm_output_str)

            agent_reply = llm_data.get("response", "I'm not sure how to reply to that right now.")
            new_facts = llm_data.get("new_facts_to_store")

            if new_facts and isinstance(new_facts, dict):
                for key, value in new_facts.items():
                    if isinstance(key, str) and isinstance(value, (str, int, float, bool)): # Basic type check
                        self.memory.add_fact(key, str(value)) # Ensure value is string for memory
                        # print(f"[DEBUG] LLM identified new fact: {key} = {value}")
                    # else:
                        # print(f"[DEBUG] LLM identified new fact with invalid type: {key} ({type(key)}) = {value} ({type(value)})")

        except json.JSONDecodeError as e:
            agent_reply = f"Sorry, I received an unexpected format from my AI brain. JSON Error: {e}. Raw output from provider: '{llm_output_str[:100]}...'"
            print(f"[ERROR] JSONDecodeError: {e}. Raw LLM output was: {llm_output_str}")
        except Exception as e:
            agent_reply = f"Sorry, an error occurred while I was thinking ({type(self.llm_provider).__name__}): {type(e).__name__} - {e}."
            print(f"[ERROR] LLM provider interaction error: {e}")

        # Log interaction (user input and final agent reply)
        self.memory.log_interaction(user_input, agent_reply)

        return agent_reply

if __name__ == '__main__':
    # Ensure your chosen LLM provider is configured via environment variables
    # (e.g., LLM_PROVIDER, OLLAMA_MODEL, OPENAI_API_KEY, etc.)
    # and that any necessary services (like Ollama server) are running.

    print("Instantiating MemoryEnhancedAgent (will use configured LLM provider)...")
    try:
        agent = MemoryEnhancedAgent()
        print(f"Agent initialized: {agent.name}")
    print(f"Starting chat with {agent.name}...")

    test_dialogue = [
        "Hello",
        "My name is Bob.",
        "I like blue.",
        "My favorite food is pizza.",
        "What is my name?",
        "What is my favorite color?",
        "What's my favorite food?",
        "I live in London",
        "Where do I live?",
        "Thanks!"
    ]

    for turn in test_dialogue:
        print(f"User: {turn}")
        response = agent.chat(turn)
        print(f"Agent: {response}")

    print("\n--- Final Memory State ---")
    print("Facts:", agent.memory.get_all_facts())
    print("History:")
    for u, a in agent.memory.get_conversation_history():
        print(f"  {u}")
        print(f"  {a}")
