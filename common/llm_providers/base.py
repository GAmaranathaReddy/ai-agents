from abc import ABC, abstractmethod
from typing import List, Dict, Any

class LLMProvider(ABC):
    """
    Abstract base class for LLM providers.
    """

    @abstractmethod
    def chat(self, model: str, messages: List[Dict[str, str]], format_json: bool = False, **kwargs: Any) -> str:
        """
        Sends a chat completion request to the LLM.

        Args:
            model: The model name or ID to use.
            messages: A list of message dictionaries, e.g.,
                      [{'role': 'user', 'content': 'Hello!'}, {'role': 'assistant', 'content': 'Hi there!'}]
            format_json: If True, attempt to instruct the model to output valid JSON.
                         Actual support depends on the provider and model.
            **kwargs: Additional provider-specific arguments.

        Returns:
            The LLM's response content as a string.
        """
        pass

    @abstractmethod
    def generate(self, model: str, prompt: str, format_json: bool = False, **kwargs: Any) -> str:
        """
        Sends a text generation (completion) request to the LLM.

        Args:
            model: The model name or ID to use.
            prompt: The prompt string for the LLM.
            format_json: If True, attempt to instruct the model to output valid JSON.
                         Actual support depends on the provider and model.
            **kwargs: Additional provider-specific arguments.

        Returns:
            The LLM's response content as a string.
        """
        pass

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"
