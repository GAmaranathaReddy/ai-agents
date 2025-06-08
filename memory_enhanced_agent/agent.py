# agent.py
import re
from memory import Memory

class MemoryEnhancedAgent:
    def __init__(self):
        self.name = "RecallBot"
        self.memory = Memory()

    def _extract_facts(self, user_input: str) -> dict:
        """
        Tries to extract key information from user_input to store as facts.
        Uses simple regular expressions.
        """
        facts_to_add = {}

        # Pattern 1: "My name is [Name]." or "I am [Name]."
        name_match = re.search(r"my name is (\w+)|i am (\w+)", user_input, re.IGNORECASE)
        if name_match:
            name = name_match.group(1) or name_match.group(2)
            if name:
                facts_to_add["name"] = name.capitalize()

        # Pattern 2: "I like [color/food/etc]." or "My favorite [thing] is [value]."
        like_match = re.search(r"i like (the color )?(\w+)", user_input, re.IGNORECASE)
        if like_match:
            # If "the color" is present, group(1) will capture it, group(2) is the color.
            # Otherwise group(1) is None, group(2) is the liked item.
            liked_item = like_match.group(2)
            if "color" in like_match.group(0).lower() or any(c in liked_item for c in ["blue", "red", "green", "yellow", "purple", "orange", "black", "white"]):
                 facts_to_add["favorite_color"] = liked_item
            else:
                facts_to_add["likes"] = liked_item # Generic like

        fav_match = re.search(r"my favorite (\w+) is (\w+)", user_input, re.IGNORECASE)
        if fav_match:
            key = f"favorite_{fav_match.group(1)}"
            value = fav_match.group(2)
            facts_to_add[key] = value

        # Pattern 3: "I live in [City/Country]."
        live_in_match = re.search(r"i live in ([\w\s]+)", user_input, re.IGNORECASE)
        if live_in_match:
            location = live_in_match.group(1).strip()
            facts_to_add["location"] = location.capitalize()

        return facts_to_add

    def _generate_response(self, user_input: str, extracted_facts: dict) -> str:
        """
        Generates a response, potentially using stored facts or acknowledging new ones.
        """
        user_name = self.memory.get_fact("name")
        greeting = f"Hello{', ' + user_name if user_name else ''}!"

        # Check for direct questions about stored facts
        if "what is my name" in user_input.lower():
            return f"{user_name}, your name is {user_name}." if user_name else "I don't think I know your name yet."

        fav_color_match = re.search(r"what is my favorite color", user_input.lower())
        if fav_color_match:
            color = self.memory.get_fact("favorite_color")
            return f"{user_name if user_name else 'Friend'}, your favorite color is {color}." if color else "I don't know your favorite color."

        fav_thing_match = re.search(r"what is my favorite (\w+)", user_input.lower())
        if fav_thing_match:
            thing_key = f"favorite_{fav_thing_match.group(1)}"
            thing_value = self.memory.get_fact(thing_key)
            if thing_value:
                return f"{user_name if user_name else 'Friend'}, your favorite {fav_thing_match.group(1)} is {thing_value}."
            else:
                return f"I don't seem to know your favorite {fav_thing_match.group(1)}."

        if "where do i live" in user_input.lower():
            location = self.memory.get_fact("location")
            return f"{user_name if user_name else 'Friend'}, you live in {location}." if location else "I don't know where you live."


        # Acknowledge newly learned facts
        if "name" in extracted_facts and extracted_facts["name"] != user_name: # If name was just learned or changed
            return f"Nice to meet you, {extracted_facts['name']}! How can I help you today?"
        if "favorite_color" in extracted_facts:
            return f"Noted, {user_name if user_name else 'friend'}! Your favorite color is {extracted_facts['favorite_color']}."
        if "likes" in extracted_facts:
            return f"Good to know you like {extracted_facts['likes']}, {user_name if user_name else 'friend'}."
        if any(key.startswith("favorite_") for key in extracted_facts):
            # Generic acknowledgement for other favorite things
            for key, value in extracted_facts.items():
                if key.startswith("favorite_"):
                    return f"Thanks for sharing that your favorite {key.split('_')[1]} is {value}, {user_name if user_name else 'friend'}!"
        if "location" in extracted_facts:
            return f"Okay, {user_name if user_name else 'friend'}, I'll remember you live in {extracted_facts['location']}."


        # Default responses
        if "hello" in user_input.lower() or "hi" in user_input.lower():
            return f"{greeting} How can I help you today?"

        if "how are you" in user_input.lower():
            return "I'm doing well, thank you for asking!"

        # Fallback response
        return f"{user_name if user_name else 'Hey there'}! You said: '{user_input}'. Ask me something else, or tell me about yourself."

    def chat(self, user_input: str) -> str:
        """
        Main chat processing method.
        """
        # 1. Try to extract facts from user input
        extracted_facts = self._extract_facts(user_input)
        acknowledged_new_fact = False
        if extracted_facts:
            for key, value in extracted_facts.items():
                # Check if this is genuinely new information or a change
                if self.memory.get_fact(key) != value:
                    self.memory.add_fact(key, value)
                    acknowledged_new_fact = True # Flag that we learned something to prioritize in response

        # 2. Generate a response
        # Pass acknowledged_new_fact or the facts themselves to _generate_response
        # to allow it to prioritize acknowledging new info.
        # For simplicity, current _generate_response checks extracted_facts directly.
        agent_response = self._generate_response(user_input, extracted_facts)

        # 4. Log interaction
        self.memory.log_interaction(user_input, agent_response)

        return agent_response

if __name__ == '__main__':
    agent = MemoryEnhancedAgent()
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
