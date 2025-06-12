from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

class BaseLLMProvider(ABC):
    """
    Abstract base class for LLM providers.
    """

    def __init__(self, api_key: Optional[str] = None, default_model: Optional[str] = None):
        """
        Initialize the provider.
        Args:
            api_key: Optional API key if required by the provider.
            default_model: Optional default model name to use if not specified in methods.
        """
        self.api_key = api_key
        self.default_model = default_model

    @abstractmethod
    def chat(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1024,
        request_json_output: bool = False,
        **kwargs: Any
    ) -> str:
        """
        Generate a chat completion.

        Args:
            messages: A list of message dictionaries, e.g., [{"role": "user", "content": "Hello"}].
            model: The specific model name to use for this request. Falls back to default_model if None.
            temperature: Sampling temperature.
            max_tokens: Maximum number of tokens to generate.
            request_json_output: If True, try to request JSON output from the model if supported.
            **kwargs: Additional provider-specific arguments.

        Returns:
            The LLM's response content as a string.

        Raises:
            NotImplementedError: If the provider does not support chat-like interactions.
            Exception: For API errors or other issues.
        """
        pass

    # Consider adding a 'generate' method for simpler prompt-in/text-out if needed later.
    # For now, 'chat' is the primary interface.

    def _get_model_name(self, model: Optional[str] = None) -> str:
        """Helper to determine the model name to use."""
        effective_model = model if model else self.default_model
        if not effective_model:
            raise ValueError("No model specified and no default model configured for this provider.")
        return effective_model
