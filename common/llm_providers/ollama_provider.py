import ollama
from .base_llm_provider import BaseLLMProvider
from typing import List, Dict, Any, Optional
import json

class OllamaProvider(BaseLLMProvider):
    """
    LLM provider for interacting with a local Ollama service.
    """

    def __init__(self, default_model: Optional[str] = "mistral", host: Optional[str] = None):
        """
        Initialize the Ollama provider.
        Args:
            default_model: The default Ollama model to use (e.g., "mistral", "llama2").
                           Ensure this model is pulled in your Ollama instance.
            host: Optional URL for the Ollama service if not default (http://localhost:11434).
        """
        super().__init__(default_model=default_model)
        # Note: The ollama.Client() call might not immediately fail if host is incorrect,
        # but subsequent calls like .chat() will.
        try:
            self.client = ollama.Client(host=host) if host else ollama.Client()
            # A simple check to see if the client can list models, indicating some connectivity.
            # This is a lightweight way to potentially catch immediate configuration issues.
            # self.client.list() # Commented out to avoid mandatory immediate check / potential startup delay
        except Exception as e:
            # This catch might be for critical init errors of the client itself, though less common.
            raise ConnectionError(f"Failed to initialize Ollama client. Ensure Ollama service is accessible. Error: {e}")


    def chat(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None, # Ollama's generate has num_predict, chat doesn't directly control max_tokens for response.
        request_json_output: bool = False,
        **kwargs: Any
    ) -> str:
        """
        Generate a chat completion using Ollama.

        Args:
            messages: A list of message dictionaries.
            model: The specific Ollama model name to use.
            temperature: Sampling temperature (Ollama calls this 'temperature').
            max_tokens: Ollama's `ollama.chat` doesn't have a direct `max_tokens` equivalent for the *response* length.
                        `ollama.generate` has `num_predict`. We can pass 'num_predict' via options.
            request_json_output: If True, request JSON output from the model.
            **kwargs: Additional options for ollama.chat (e.g., 'options': {'num_predict': max_tokens}).

        Returns:
            The LLM's response content as a string.

        Raises:
            ollama.ResponseError: For errors from the Ollama API (e.g., model not found, connection issues).
            json.JSONDecodeError: If `request_json_output` is True but the response is not valid JSON.
            Exception: For other issues.
        """
        effective_model = self._get_model_name(model)

        options = kwargs.pop('options', {}) # Get existing options dict or create new
        if temperature is not None: # Ollama default is 0.8 if not set
            options['temperature'] = temperature
        if max_tokens is not None:
            # For `ollama.chat`, `num_predict` in options might influence length for some models,
            # but it's not a guaranteed token limit for the chat response itself.
            options['num_predict'] = max_tokens
        # Other common options: top_p, top_k, stop sequences etc. can be added to `options`

        try:
            # print(f"[OllamaProvider DEBUG] Request: model={effective_model}, messages={messages}, format={'json' if request_json_output else ''}, options={options}, kwargs={kwargs}")
            response = self.client.chat(
                model=effective_model,
                messages=messages,
                format='json' if request_json_output else '', # Empty string for default text format
                options=options if options else None, # Pass options only if there are any
                **kwargs # Pass any other specific kwargs for ollama.chat
            )

            content = response['message']['content']

            # If JSON output was requested, try to parse to validate.
            # The method contract is to return a string, so we don't return the parsed object directly.
            # The caller is responsible for parsing if they expect JSON.
            if request_json_output:
                try:
                    json.loads(content)
                except json.JSONDecodeError as e:
                    # This indicates the LLM failed to produce valid JSON despite being asked.
                    # Re-raise as a specific error or a more general one.
                    # print(f"Warning: OllamaProvider received non-JSON response when JSON was requested for model {effective_model}. Content: {content[:100]}...")
                    raise json.JSONDecodeError(
                        f"LLM ({effective_model}) was asked for JSON but returned non-JSON: {content[:100]}...",
                        doc=content, # Original document
                        pos=0 # Position of error (unknown here)
                    )

            return content
        except ollama.ResponseError as e:
            # Handle cases like model not found, connection errors more specifically
            # print(f"Ollama ResponseError: Status Code: {e.status_code}, Error: {e.error}")
            if "model not found" in e.error.lower():
                 raise ollama.ResponseError(f"Model '{effective_model}' not found by Ollama. Please pull the model. Original error: {e.error}", status_code=e.status_code) from e
            raise  # Re-raise other Ollama specific errors
        except Exception as e:
            # Catch-all for other unexpected errors, e.g., network issues not caught by ollama.Client
            # print(f"Unexpected error during Ollama chat completion: {type(e).__name__} - {e}")
            raise Exception(f"Unexpected error during Ollama chat completion with model {effective_model}: {e}")
