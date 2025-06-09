import ollama # Added for Ollama integration

class LLMEnhancedAgent:
    def __init__(self, llm_service_name="Ollama", model_name="mistral"):
        """
        Initializes the LLM-Enhanced Agent.

        Args:
            llm_service_name (str): The name of the LLM service being used.
            model_name (str): The specific Ollama model to use (e.g., "mistral", "llama2").
        """
        self.llm_service_name = llm_service_name
        self.model_name = model_name # Default model

    def get_llm_response(self, user_input: str) -> str:
        """
        Gets a response from the configured Ollama LLM.

        Args:
            user_input (str): The input string from the user.

        Returns:
            str: The LLM's response or an error message if interaction fails.
        """
        try:
            # Construct a simple prompt or use user_input directly
            # For more complex interactions, you might build a more structured prompt.
            prompt = f"User query: \"{user_input}\". Respond to this query."

            response = ollama.chat(
                model=self.model_name,
                messages=[
                    {
                        'role': 'user',
                        'content': user_input, # Sending user_input directly as content
                    }
                ]
            )
            return response['message']['content']
        except Exception as e:
            # Log the full error for debugging if needed, but return a user-friendly message
            # print(f"Ollama interaction error: {e}")
            return f"Error interacting with Ollama ({self.model_name}): {type(e).__name__}. Is Ollama running and the model '{self.model_name}' pulled?"

    def process_request(self, user_input: str) -> str:
        """
        Processes the user's request by first getting a response from the LLM
        and then potentially adding more agent-specific logic.

        Args:
            user_input (str): The input string from the user.

        Returns:
            str: The agent's final response.
        """
        llm_output = self.get_llm_response(user_input)

        # Agent-specific logic can be added here.
        # For example, the agent might format the LLM output,
        # or combine it with information from other sources.
        final_response = f"Agent: Here's what the LLM ({self.llm_service_name}) came up with: {llm_output}"
        return final_response

if __name__ == '__main__':
    # Example usage (optional, primarily for testing the agent directly)
    # Ensure Ollama is running and the model (e.g., "mistral") is pulled.
    # Example: ollama pull mistral
    agent = LLMEnhancedAgent() # Uses default "mistral"

    test_input = "Hello, world! What is the capital of France?"
    print(f"User Input: {test_input}")
    # Direct call to get_llm_response for testing the Ollama part
    # llm_response = agent.get_llm_response(test_input)
    # print(f"Direct LLM Response: {llm_response}")

    # Test the full process_request
    response = agent.process_request(test_input)
    print(f"Agent Response: {response}")

    test_input_2 = "Tell me a short story about a brave robot."
    print(f"\nUser Input: {test_input_2}")
    response_2 = agent.process_request(test_input_2)
    print(f"Agent Response: {response_2}")

    test_input_3 = "What is 1+1?" # Test with a model that might not be good at math
    print(f"\nUser Input: {test_input_3}")
    agent_custom_model = LLMEnhancedAgent(model_name="nous-hermes2") # Example for a different model
    # Make sure "nous-hermes2" is pulled: ollama pull nous-hermes2
    # response_3 = agent_custom_model.process_request(test_input_3)
    # print(f"Agent (nous-hermes2) Response: {response_3}")
    # Using default model for actual test run to avoid dependency on too many models
    response_3_default = agent.process_request(test_input_3)
    print(f"Agent ({agent.model_name}) Response: {response_3_default}")
