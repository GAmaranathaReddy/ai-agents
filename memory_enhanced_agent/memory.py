# memory.py
from typing import List, Dict, Tuple, Optional

class Memory:
    def __init__(self):
        """
        Initializes the Memory module.
        - facts: Stores key-value pairs of information.
        - conversation_history: Stores a log of user-agent interactions.
        """
        self._facts: Dict[str, str] = {}
        self._conversation_history: List[Tuple[str, str]] = []

    def add_fact(self, key: str, value: str) -> None:
        """
        Adds or updates a fact in the memory.
        """
        key_lower = key.lower()
        self._facts[key_lower] = value
        # print(f"[Memory DEBUG] Added fact: {key_lower} = {value}") # For debugging

    def get_fact(self, key: str) -> Optional[str]:
        """
        Retrieves a fact from the memory. Returns None if the fact is not found.
        """
        key_lower = key.lower()
        return self._facts.get(key_lower)

    def log_interaction(self, user_input: str, agent_response: str) -> None:
        """
        Logs a user input and the agent's response to the conversation history.
        """
        self._conversation_history.append(("user: " + user_input, "agent: " + agent_response))

    def get_conversation_history(self) -> List[Tuple[str, str]]:
        """
        Returns the entire conversation history.
        """
        return self._conversation_history

    def get_last_n_interactions(self, n: int) -> List[Tuple[str, str]]:
        """
        Returns the last N interactions from the conversation history.
        """
        return self._conversation_history[-n:]

    def clear_facts(self) -> None:
        """Clears all stored facts."""
        self._facts.clear()

    def clear_history(self) -> None:
        """Clears the conversation history."""
        self._conversation_history.clear()

    def get_all_facts(self) -> Dict[str, str]:
        """Returns all stored facts."""
        return self._facts.copy()

if __name__ == '__main__':
    print("Testing Memory class...")
    memory_module = Memory()

    # Test facts
    memory_module.add_fact("name", "Alice")
    memory_module.add_fact("favorite_color", "blue")
    print(f"Fact 'name': {memory_module.get_fact('name')}")
    print(f"Fact 'Favorite_Color': {memory_module.get_fact('Favorite_Color')}") # Test case-insensitivity
    print(f"Fact 'age': {memory_module.get_fact('age')}") # Test non-existent fact

    all_facts = memory_module.get_all_facts()
    print(f"All facts: {all_facts}")

    # Test conversation history
    memory_module.log_interaction("Hello", "Hi there!")
    memory_module.log_interaction("What's my name?", "Your name is Alice.")

    history = memory_module.get_conversation_history()
    print("\nConversation History:")
    for user, agent in history:
        print(f"  {user}")
        print(f"  {agent}")

    last_interaction = memory_module.get_last_n_interactions(1)
    print(f"\nLast 1 interaction: {last_interaction}")

    # Test clearing
    memory_module.clear_facts()
    memory_module.clear_history()
    print(f"\nAll facts after clearing: {memory_module.get_all_facts()}")
    print(f"History after clearing: {memory_module.get_conversation_history()}")
