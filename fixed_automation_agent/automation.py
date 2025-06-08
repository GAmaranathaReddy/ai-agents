import re

class FixedAutomationAgent:
    def __init__(self):
        """
        Initializes the Fixed Automation Agent.
        This agent operates based on predefined rules.
        """
        self.name = "RuleBot V1"

    def process_request(self, user_input: str) -> str:
        """
        Processes the user's request based on a fixed set of rules.

        Args:
            user_input (str): The input string from the user.

        Returns:
            str: The agent's response based on its rules.
        """
        user_input_lower = user_input.lower()

        # Rule 1: Greeting
        if user_input_lower in ["hi", "hello", "hey", "greetings"]:
            return f"Hello! I am {self.name}. I can perform simple calculations like 'add X Y' or tell you about myself if you type 'about'."

        # Rule 2: About the agent
        if user_input_lower == "about":
            return f"I am {self.name}, a simple Fixed Automation Agent. I respond to specific commands based on my programming."

        # Rule 3: Simple addition command "add X Y"
        # Using regex to parse "add <number1> <number2>"
        match = re.match(r"add\s+(\d+)\s+(\d+)", user_input_lower)
        if match:
            num1 = int(match.group(1))
            num2 = int(match.group(2))
            result = num1 + num2
            return f"The sum of {num1} and {num2} is {result}."

        # Rule 4: Simple multiplication command "multiply X Y"
        match_multiply = re.match(r"multiply\s+(\d+)\s+(\d+)", user_input_lower)
        if match_multiply:
            num1 = int(match_multiply.group(1))
            num2 = int(match_multiply.group(2))
            result = num1 * num2
            return f"The product of {num1} and {num2} is {result}."

        # Default response if no rules match
        return "I'm sorry, I don't understand that command. Try 'add X Y', 'multiply X Y', 'about', or say 'hello'."

if __name__ == '__main__':
    # Example usage (optional, primarily for testing the agent directly)
    agent = FixedAutomationAgent()

    commands = [
        "hello",
        "add 10 5",
        "multiply 3 4",
        "about",
        "what is the weather?",
        "add 7 and 3", # Should fail
        "multiply 2 by 6" # Should fail
    ]

    for cmd in commands:
        response = agent.process_request(cmd)
        print(f"User: {cmd}")
        print(f"Agent: {response}\n")

    # Test specific cases
    print(f"User: add 1 2")
    print(f"Agent: {agent.process_request('add 1 2')}\n")

    print(f"User: multiply 100 2")
    print(f"Agent: {agent.process_request('multiply 100 2')}\n")
