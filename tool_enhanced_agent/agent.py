# agent.py
import re
from tools import get_current_datetime, calculate_sum, get_weather

class ToolEnhancedAgent:
    def __init__(self):
        self.name = "ToolBot Alpha"

    def process_request(self, user_input: str) -> str:
        """
        Processes the user's request by parsing it, deciding which tool to use (if any),
        executing the tool, and formulating a response.
        """
        user_input_lower = user_input.lower()
        thought_process = [f"Received input: '{user_input}'"]

        # 1. Check for "time" or "date" -> get_current_datetime
        if "time" in user_input_lower or "date" in user_input_lower or "datetime" in user_input_lower:
            thought_process.append("Decision: Matched 'time/date' keyword. Using get_current_datetime tool.")
            tool_output = get_current_datetime()
            return f"The current date and time is: {tool_output}"

        # 2. Check for "sum" or "add" (with numbers) -> calculate_sum
        # Regex to find "sum/add" followed by two numbers (integers or decimals)
        sum_match = re.search(r"(?:sum|add|calculate|plus)\s(?:of\s)?(-?\d+(?:\.\d+)?)\s(?:and|plus|\+)\s(-?\d+(?:\.\d+)?)", user_input_lower)
        if sum_match:
            num1_str, num2_str = sum_match.groups()
            thought_process.append(f"Decision: Matched 'sum/add' pattern. Numbers found: {num1_str}, {num2_str}. Using calculate_sum tool.")
            try:
                num1 = float(num1_str)
                num2 = float(num2_str)
                tool_output = calculate_sum(num1, num2)
                return tool_output
            except ValueError:
                thought_process.append("Error: Could not convert parsed numbers to float.")
                return "I found numbers, but couldn't understand them properly for calculation. Please use valid numbers."

        # 3. Check for "weather" (with a city name) -> get_weather
        # Regex to find "weather in/for <city_name>" or "what's the weather in <city_name>"
        # This regex will capture the city name. It tries to capture multiple words for city name.
        weather_match = re.search(r"weather\s(?:in|for)\s([a-zA-Z\s]+)(?:\?|$)", user_input_lower)
        if not weather_match: # Try another pattern like "what is the weather in city"
             weather_match = re.search(r"what's\s(?:the\s)?weather\s(?:in|for)\s([a-zA-Z\s]+)(?:\?|$)", user_input_lower)

        if weather_match:
            city_name = weather_match.group(1).strip()
            if city_name:
                thought_process.append(f"Decision: Matched 'weather' pattern. City found: '{city_name}'. Using get_weather tool.")
                tool_output = get_weather(city_name)
                return tool_output
            else:
                thought_process.append("Info: Matched 'weather' pattern but no city name was captured.")
                return "I can get the weather for you, but please specify a city name, like 'weather in London'."


        # Default response if no tool is matched
        thought_process.append("Decision: No specific tool matched the input.")
        return f"I am {self.name}. I can tell you the time, sum numbers (e.g., 'add 5 and 3'), or get the weather (e.g., 'weather in Paris'). How can I help?"

if __name__ == '__main__':
    agent = ToolEnhancedAgent()

    test_queries = [
        "Hello there!",
        "What time is it?",
        "current date please",
        "Calculate the sum of 10 and 25.5",
        "add -5 plus 3.2",
        "sum of 100 and 200",
        "What's the weather in London?",
        "weather for New York please",
        "weather in Berlin?",
        "sum of ten and five", # Should fail sum tool due to non-numeric
        "weather in", # Should ask for city
        "weather for ?" # Should ask for city
    ]

    for query in test_queries:
        response = agent.process_request(query)
        print(f"User: {query}")
        # The thought process is internal to the agent method in this setup
        # To see thoughts, you'd need to modify process_request to return them
        print(f"Agent: {response}\n" + "-"*30)

    print(f"User: add 5 and 3") # Specific test for sum without "calculate" or "the"
    print(f"Agent: {agent.process_request('add 5 and 3')}\n" + "-"*30)

    print(f"User: what is the weather in San Francisco")
    print(f"Agent: {agent.process_request('what is the weather in San Francisco')}\n" + "-"*30)
