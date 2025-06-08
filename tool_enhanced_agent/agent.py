# agent.py
import re
from tools import get_current_datetime, calculate_sum, get_weather

class ToolEnhancedAgent:
    def __init__(self):
        self.name = "ToolBot Alpha"

    def process_request(self, user_input: str) -> dict:
        """
        Processes the user's request by parsing it, deciding which tool to use (if any),
        executing the tool, and formulating a response.
        Returns a dictionary with details of the processing.
        """
        user_input_lower = user_input.lower()
        # thought_process = [f"Received input: '{user_input}'"] # Internal thought process, not directly returned for now

        response_dict = {
            "user_input": user_input,
            "tool_used": None,
            "tool_input_params": None,
            "tool_output_raw": None,
            "final_response": None,
            "error": None
        }

        # 1. Check for "time" or "date" -> get_current_datetime
        if "time" in user_input_lower or "date" in user_input_lower or "datetime" in user_input_lower:
            response_dict["tool_used"] = "get_current_datetime"
            raw_output = get_current_datetime()
            response_dict["tool_output_raw"] = raw_output
            response_dict["final_response"] = f"The current date and time is: {raw_output}"
            return response_dict

        # 2. Check for "sum" or "add" (with numbers) -> calculate_sum
        sum_match = re.search(r"(?:sum|add|calculate|plus)\s(?:of\s)?(-?\d+(?:\.\d+)?)\s(?:and|plus|\+)\s(-?\d+(?:\.\d+)?)", user_input_lower)
        if sum_match:
            num1_str, num2_str = sum_match.groups()
            response_dict["tool_used"] = "calculate_sum"
            response_dict["tool_input_params"] = {"a": num1_str, "b": num2_str}
            try:
                num1 = float(num1_str)
                num2 = float(num2_str)
                raw_output = calculate_sum(num1, num2) # This tool already returns a formatted string
                response_dict["tool_output_raw"] = raw_output # Storing the already formatted string
                response_dict["final_response"] = raw_output # Using it directly
                if "Error:" in raw_output: # Check if the tool itself reported an error
                    response_dict["error"] = raw_output
            except ValueError:
                response_dict["error"] = "Invalid number format for sum calculation."
                response_dict["final_response"] = "I found numbers, but couldn't understand them properly for calculation. Please use valid numbers."
            return response_dict

        # 3. Check for "weather" (with a city name) -> get_weather
        weather_match = re.search(r"weather\s(?:in|for)\s([a-zA-Z\s]+)(?:\?|$)", user_input_lower)
        if not weather_match:
             weather_match = re.search(r"what's\s(?:the\s)?weather\s(?:in|for)\s([a-zA-Z\s]+)(?:\?|$)", user_input_lower)

        if weather_match:
            city_name = weather_match.group(1).strip()
            response_dict["tool_used"] = "get_weather"
            if city_name:
                response_dict["tool_input_params"] = {"city": city_name}
                raw_output = get_weather(city_name) # This tool already returns a formatted string
                response_dict["tool_output_raw"] = raw_output
                response_dict["final_response"] = raw_output
                if "Error:" in raw_output:
                    response_dict["error"] = raw_output
            else:
                response_dict["error"] = "No city name provided with weather command."
                response_dict["final_response"] = "I can get the weather for you, but please specify a city name, like 'weather in London'."
            return response_dict

        # Default response if no tool is matched
        response_dict["final_response"] = f"I am {self.name}. I can tell you the time, sum numbers (e.g., 'add 5 and 3'), or get the weather (e.g., 'weather in Paris'). How can I help?"
        return response_dict

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
        "sum of ten and five", # Should fail sum tool due to non-numeric (handled by current regex)
        "add abc and 123", # Test error in calculate_sum via string input
        "weather in", # Should ask for city
        "weather for ?" # Should ask for city
    ]

    for query in test_queries:
        results = agent.process_request(query)
        print(f"User Query: \"{results['user_input']}\"")
        if results['tool_used']:
            print(f"  Tool Used: {results['tool_used']}")
            if results['tool_input_params']:
                print(f"  Tool Input: {results['tool_input_params']}")
            if results['tool_output_raw']:
                print(f"  Tool Raw Output: {results['tool_output_raw']}")
        if results['error']:
            print(f"  Error: {results['error']}")
        print(f"  Agent Final Response: {results['final_response']}")
        print("-" * 30 + "\n")

    # Specific test for sum without "calculate" or "the"
    # results = agent.process_request('add 5 and 3') # Already covered by loop
    # print(f"User Query: \"{results['user_input']}\" -> Final Response: {results['final_response']}\n" + "-"*30)

    # results = agent.process_request('what is the weather in San Francisco') # Already covered
    # print(f"User Query: \"{results['user_input']}\" -> Final Response: {results['final_response']}\n" + "-"*30)
