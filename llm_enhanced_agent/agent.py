# agent.py
# Uses the new LLM abstraction layer from common.llm_providers
from common.llm_providers.client import get_llm_client, SUPPORTED_PROVIDERS, DEFAULT_PROVIDER
from typing import List, Dict, Optional # For type hinting

class LLMEnhancedAgent:
    def __init__(self, provider_name: Optional[str] = None, model_name: Optional[str] = None, **provider_kwargs):
        """
        Initializes the LLM-Enhanced Agent using a specified provider and model
        via the common LLM client factory.

        Args:
            provider_name (str, optional): Name of the LLM provider (e.g., "ollama", "openai").
                                           Defaults to DEFAULT_PROVIDER from client.py or LLM_PROVIDER env var.
            model_name (str, optional): The specific model name to use for this agent.
            **provider_kwargs: Additional keyword arguments for the provider's constructor
                               (e.g., api_key for OpenAI/Gemini, region_name for Bedrock).
        """
        try:
            # Pass provider_kwargs which might include 'api_key', 'region_name', or 'default_model' for the provider itself
            self.llm_client = get_llm_client(provider_name, **provider_kwargs)
            # Get the actual provider name from the client instance for display/logging
            self.actual_provider_name = self.llm_client.__class__.__name__.replace("Provider", "")
        except Exception as e:
            print(f"FATAL: Error initializing LLM client for provider '{provider_name or DEFAULT_PROVIDER}': {e}")
            print("Ensure necessary API keys (e.g., OPENAI_API_KEY, GOOGLE_API_KEY) or configurations (AWS, Ollama) are set.")
            # This is a critical failure, re-raise or handle as appropriate for the application
            raise RuntimeError(f"Failed to initialize LLM client: {e}") from e

        # Determine the model name to be used by this agent instance
        if model_name:
            self.model_name = model_name
        # If model_name is not provided, try to use default_model from the provider if it was set by provider_kwargs
        elif hasattr(self.llm_client, 'default_model') and self.llm_client.default_model:
            self.model_name = self.llm_client.default_model
        else: # Fallback to provider-specific defaults if no model_name and provider's default_model isn't useful
            if self.actual_provider_name.lower() == "ollama":
                self.model_name = "mistral"
            elif self.actual_provider_name.lower() == "openai":
                self.model_name = "gpt-3.5-turbo"
            elif self.actual_provider_name.lower() == "gemini":
                self.model_name = "gemini-pro"
            elif self.actual_provider_name.lower() == "bedrock":
                # Bedrock default model is often set in its constructor, this is another fallback
                self.model_name = "anthropic.claude-3-sonnet-20240229-v1:0"
            else:
                # This case should ideally be handled by get_llm_client or provider's __init__
                # if a model is strictly required for initialization.
                raise ValueError(f"No model_name specified and could not determine a default for provider '{self.actual_provider_name}'.")

        self.name = f"LLMEnhancedAgent ({self.actual_provider_name}/{self.model_name})"
        self.llm_service_name = self.name # For display in process_request

    def get_llm_response(self, user_input: str) -> str:
        """
        Gets a response from the configured LLM provider using the agent's model.

        Args:
            user_input (str): The input string from the user.

        Returns:
            str: The LLM's response or an error message if interaction fails.
        """
        messages: List[Dict[str, str]] = [{'role': 'user', 'content': user_input}]
        try:
            response_content = self.llm_client.chat(
                model=self.model_name, # Use the agent's configured model
                messages=messages
                # format_json=False is default.
                # Other parameters like temperature, max_tokens can be passed here if desired,
                # or set as defaults in the provider via get_llm_client's kwargs.
            )
            return response_content
        except Exception as e:
            # print(f"LLM interaction error with {self.actual_provider_name} model {self.model_name}: {e}")
            return f"Error interacting with LLM ({self.actual_provider_name}/{self.model_name}): {type(e).__name__} - {e}"

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
    # The agent now uses the globally configured LLM provider.
    # Ensure your desired provider is configured via environment variables
    # (e.g., LLM_PROVIDER, OLLAMA_MODEL, OPENAI_API_KEY, etc.)
    # See common/llm_config.py and the main project README for details.

    print("Instantiating LLMEnhancedAgent (will use configured provider)...")
    try:
        agent = LLMEnhancedAgent()
        print(f"Agent initialized: {agent.name}")

        test_input = "Hello, world! What is the capital of France?"
        print(f"\nUser Input: {test_input}")
        response = agent.process_request(test_input)
        print(f"Agent Response: {response}")

        test_input_2 = "Tell me a short story about a brave robot."
        print(f"\nUser Input: {test_input_2}")
        response_2 = agent.process_request(test_input_2)
        print(f"Agent Response: {response_2}")

        test_input_3 = "What is 1+1?"
        print(f"\nUser Input: {test_input_3}")
        response_3 = agent.process_request(test_input_3)
        print(f"Agent Response: {response_3}")

    except ValueError as ve: # Catch config errors from get_llm_provider_instance
        print(f"Configuration Error: {ve}")
        print("Please ensure your LLM provider environment variables are set correctly.")
    except Exception as e: # Catch other errors like connection issues
        print(f"An error occurred during testing: {type(e).__name__} - {e}")
