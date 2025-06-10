import ollama
import json
import re # Retain for number extraction if LLM provides text, or as fallback

class FixedAutomationAgent:
    def __init__(self, llm_model="mistral"):
        """
        Initializes the Fixed Automation Agent with LLM for NLU.
        """
        self.name = "RuleBot V2 (LLM-Enhanced)"
        self.llm_model = llm_model
        self.tasks = ["greet", "about", "add", "multiply", "unknown"]

    def _perform_greeting(self) -> str:
        return f"Hello! I am {self.name}. I can help with greetings, info about myself, addition, and multiplication."

    def _perform_about(self) -> str:
        return f"I am {self.name}, an agent that uses an LLM to understand commands for a fixed set of tasks."

    def _perform_addition(self, num1: float, num2: float) -> str:
        try:
            result = float(num1) + float(num2)
            return f"The sum of {num1} and {num2} is {result}."
        except ValueError:
            return "Error: Invalid numbers provided for addition."

    def _perform_multiplication(self, num1: float, num2: float) -> str:
        try:
            result = float(num1) * float(num2)
            return f"The product of {num1} and {num2} is {result}."
        except ValueError:
            return "Error: Invalid numbers provided for multiplication."

    def process_request(self, user_input: str) -> dict:
        """
        Processes the user's request by using an LLM to interpret the command,
        then executing a predefined action.
        Returns a dictionary containing LLM interpretation, final result, and any errors.
        """
        response_payload = {
            "user_input": user_input,
            "llm_interpretation": None,
            "final_result": None,
            "error": None
        }

        # Prompt for the LLM to classify task and extract entities
        prompt_to_llm = f"""Analyze the user input: "{user_input}"
        Identify which of the following tasks the user wants to perform: {', '.join(self.tasks)}.
        If the task is 'add' or 'multiply', extract exactly two numbers.
        Respond in JSON format with "task" and "numbers" (as a list of numbers, or null if not applicable).
        Example for 'add 10 and 5': {{"task": "add", "numbers": [10, 5]}}
        Example for 'hello': {{"task": "greet", "numbers": null}}
        Example for 'what is 2 times 3?': {{"task": "multiply", "numbers": [2, 3]}}
        If the input is unclear or doesn't match a task, set task to "unknown".
        Only provide the JSON response.
        """

        try:
            ollama_response = ollama.chat(
                model=self.llm_model,
                messages=[{'role': 'user', 'content': prompt_to_llm}],
                format='json'
            )
            llm_output_str = ollama_response['message']['content']
            # print(f"LLM Raw Output: {llm_output_str}") # For debugging
            llm_output_json = json.loads(llm_output_str)
            response_payload["llm_interpretation"] = llm_output_json

            task = llm_output_json.get("task")
            numbers = llm_output_json.get("numbers")

            if task == "greet":
                response_payload["final_result"] = self._perform_greeting()
            elif task == "about":
                response_payload["final_result"] = self._perform_about()
            elif task == "add":
                if isinstance(numbers, list) and len(numbers) == 2:
                    response_payload["final_result"] = self._perform_addition(*numbers)
                else:
                    response_payload["error"] = "Addition task identified, but could not extract two valid numbers from LLM output."
                    response_payload["final_result"] = "I understood you want to add, but I need two numbers. Example: 'add 10 and 5'."
            elif task == "multiply":
                if isinstance(numbers, list) and len(numbers) == 2:
                    response_payload["final_result"] = self._perform_multiplication(*numbers)
                else:
                    response_payload["error"] = "Multiplication task identified, but could not extract two valid numbers from LLM output."
                    response_payload["final_result"] = "I understood you want to multiply, but I need two numbers. Example: 'multiply 7 by 3'."
            else: # task == "unknown" or other
                response_payload["final_result"] = "Sorry, I couldn't map your request to a known task. I can greet, tell you about me, add, or multiply."
                if not response_payload["error"] and task != "unknown":
                     response_payload["error"] = f"LLM identified task as '{task}', but it's not handled or number extraction failed."


        except json.JSONDecodeError as e:
            response_payload["error"] = f"LLM output was not valid JSON: {e}. Raw output: {llm_output_str}"
            response_payload["final_result"] = "Sorry, I had trouble understanding the structure of the command."
        except Exception as e:
            response_payload["error"] = f"Ollama LLM error: {type(e).__name__} - {e}. Is Ollama running and model '{self.llm_model}' pulled?"
            response_payload["final_result"] = "Sorry, I'm having trouble connecting to my understanding module."

        return response_payload

if __name__ == '__main__':
    # Ensure Ollama is running and the model (e.g., "mistral") is pulled.
    # Example: ollama pull mistral
    agent = FixedAutomationAgent()

    commands_to_test = [
        "hello there",
        "tell me about yourself",
        "what is 5 plus 3?",
        "can you calculate 10 added to 7",
        "multiply 4 by 6",
        "what's 100 times 2?",
        "what is the weather like today?", # Should be 'unknown'
        "sum of 10, 20, and 30", # Should ideally fail number extraction or be handled by LLM
        "add ten and five" # Test LLM's ability to convert text to number
    ]

    for cmd_text in commands_to_test:
        print(f"User: {cmd_text}")
        result_payload = agent.process_request(cmd_text)
        print(f"  LLM Interpretation: {result_payload['llm_interpretation']}")
        if result_payload['error']:
            print(f"  Error: {result_payload['error']}")
        print(f"  Agent Final Result: {result_payload['final_result']}\n")
