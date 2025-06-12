# agent.py
# import ollama # No longer directly importing ollama
from common import get_llm_provider_instance # Use the abstraction layer
import json
import re # Can still be useful for simple fallbacks or specific parsing if LLM fails
from tools import get_current_datetime, calculate_sum, get_weather

class ToolEnhancedAgent:
    def __init__(self): # LLM model is now configured via the provider
        self.llm_provider = get_llm_provider_instance()
        self.name = f"ToolBot Pro (using {type(self.llm_provider).__name__})"
        # self.llm_model = llm_model # Removed, provider handles its own model config
        self.tools_description = {
            "get_current_datetime": "Gets the current date and time. No arguments needed.",
            "calculate_sum": "Calculates the sum of two numbers. Expects two numerical arguments named 'a' and 'b'.",
            "get_weather": "Gets the dummy weather forecast for a given city. Expects one string argument named 'city'.",
            "unknown": "Use this if no other tool seems appropriate for the user's request."
        }
        self.callable_tools = {
            "get_current_datetime": get_current_datetime,
            "calculate_sum": calculate_sum,
            "get_weather": get_weather
        }

    def process_request(self, user_input: str) -> dict:
        """
        Processes the user's request using an LLM to select a tool and extract arguments,
        then executes the tool and formulates a response.
        Returns a dictionary with details of the processing.
        """
        response_payload = {
            "user_input": user_input,
            "llm_interpretation": None,
            "tool_used": None,
            "tool_input_params": None,
            "tool_output_raw": None,
            "final_response": None,
            "error": None
        }

        tools_prompt_info = "\n".join([f"- '{name}': {desc}" for name, desc in self.tools_description.items()])

        prompt_to_llm = f"""Given the user input: "{user_input}"
Analyze the input and determine which of the following tools is most appropriate to use.
Available tools:
{tools_prompt_info}

If a tool requires arguments, extract them from the user input.
Respond in JSON format with "tool_name" and "arguments" (as a dictionary, or an empty dictionary if no arguments are needed).
If the 'calculate_sum' tool is chosen, the arguments dictionary should be like {{"a": number1, "b": number2}}.
If the 'get_weather' tool is chosen, the arguments dictionary should be like {{"city": "city_name"}}.
If 'get_current_datetime' is chosen, arguments should be {{}}.
If no tool is suitable, use "unknown" as the tool_name.

Example for 'What is 10 plus 5?': {{"tool_name": "calculate_sum", "arguments": {{"a": 10, "b": 5}}}}
Example for 'current time': {{"tool_name": "get_current_datetime", "arguments": {{}}}}
Example for 'weather in Berlin': {{"tool_name": "get_weather", "arguments": {{"city": "Berlin"}}}}
Example for 'hello how are you': {{"tool_name": "unknown", "arguments": {{}}}}

Only provide the JSON response.
"""

        try:
            # ollama_response = ollama.chat( # Old call
            #     model=self.llm_model,
            #     messages=[{'role': 'user', 'content': prompt_to_llm}],
            #     format='json'
            # )
            # llm_output_str = ollama_response['message']['content']
            llm_output_str = self.llm_provider.chat(
                messages=[{'role': 'user', 'content': prompt_to_llm}],
                request_json_output=True # Signal to provider to request JSON
            )
            # print(f"LLM Raw Output: {llm_output_str}") # For debugging
            # Provider should raise error if JSON was requested but not received (for providers that support enforced JSON mode).
            # For others, it's best effort via prompt, so json.loads might fail here.
            llm_output_json = json.loads(llm_output_str)
            response_payload["llm_interpretation"] = llm_output_json

            tool_name = llm_output_json.get("tool_name")
            arguments = llm_output_json.get("arguments", {}) # Default to empty dict

            response_payload["tool_used"] = tool_name
            response_payload["tool_input_params"] = arguments if arguments else None


            if tool_name in self.callable_tools:
                tool_function = self.callable_tools[tool_name]
                # Ensure arguments are passed correctly, especially for no-arg functions
                if not arguments and tool_name == "get_current_datetime": # No args expected
                    raw_output = tool_function()
                elif arguments: # Arguments are expected and provided
                     # For calculate_sum, ensure 'a' and 'b' are floats if they come as strings from LLM
                    if tool_name == "calculate_sum":
                        try:
                            args_for_sum = {k: float(v) for k, v in arguments.items()}
                            raw_output = tool_function(**args_for_sum)
                        except (ValueError, TypeError) as e:
                            response_payload["error"] = f"Invalid number format for sum: {arguments}. Error: {e}"
                            raw_output = f"Error: Could not perform sum with provided numbers {arguments}."
                    else: # For get_weather, pass arguments as is
                        raw_output = tool_function(**arguments)
                else: # Tool expects args but none provided by LLM
                    response_payload["error"] = f"Tool '{tool_name}' expects arguments, but LLM provided none or they were invalid."
                    raw_output = f"Error: Missing arguments for tool {tool_name}."

                response_payload["tool_output_raw"] = raw_output

                # Formulate final response (can be same as raw_output if tool returns formatted string)
                if "Error:" not in raw_output: # Simple check if tool itself signaled an error
                    if tool_name == "get_current_datetime":
                        response_payload["final_response"] = f"The current date and time is: {raw_output}."
                    else: # For sum and weather, the tools already return formatted strings
                        response_payload["final_response"] = raw_output
                else:
                    response_payload["final_response"] = raw_output # Pass tool's error message
                    if not response_payload["error"]: # If agent didn't set an error yet
                         response_payload["error"] = raw_output


            elif tool_name == "unknown":
                response_payload["final_response"] = f"I'm not sure how to help with that. I can tell time, sum numbers, or get weather. Your input: \"{user_input}\""
            else:
                response_payload["error"] = f"LLM selected an unknown or unhandled tool: '{tool_name}'."
                response_payload["final_response"] = "Sorry, I tried to use a tool I don't recognize."

        except json.JSONDecodeError as e:
            response_payload["error"] = f"LLM output was not valid JSON: {e}. Raw output from provider: {llm_output_str}"
            response_payload["final_response"] = "Sorry, I had trouble understanding the structure of the command from my AI."
        except Exception as e:
            response_payload["error"] = f"LLM provider error ({type(self.llm_provider).__name__}): {type(e).__name__} - {e}."
            response_payload["final_response"] = "Sorry, I'm having trouble connecting to my understanding module."

        return response_payload

if __name__ == '__main__':
    # Ensure your chosen LLM provider is configured via environment variables
    # (e.g., LLM_PROVIDER, OLLAMA_MODEL, OPENAI_API_KEY, etc.)
    # and that any necessary services (like Ollama server) are running.

    print("Instantiating ToolEnhancedAgent (will use configured LLM provider)...")
    try:
        agent = ToolEnhancedAgent()
        print(f"Agent initialized: {agent.name}")

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

    except ValueError as ve: # Catch config errors from get_llm_provider_instance
        print(f"Configuration Error: {ve}")
        print("Please ensure your LLM provider environment variables are set correctly.")
    except Exception as e: # Catch other errors like connection issues during init or first call
        print(f"An error occurred during testing: {type(e).__name__} - {e}")
