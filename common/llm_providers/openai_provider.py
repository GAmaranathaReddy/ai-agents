import openai # Alternatively, from openai import OpenAI
import os
from .base_llm_provider import BaseLLMProvider
from typing import List, Dict, Any, Optional
import json

class OpenAIProvider(BaseLLMProvider):
    """
    LLM provider for interacting with OpenAI models (GPT-3.5, GPT-4, etc.).
    """

    def __init__(self, api_key: Optional[str] = None, default_model: Optional[str] = "gpt-3.5-turbo"):
        """
        Initialize the OpenAI provider.
        Args:
            api_key: OpenAI API key. If None, attempts to load from OPENAI_API_KEY env var.
            default_model: Default OpenAI model to use.
        """
        resolved_api_key = api_key if api_key else os.environ.get("OPENAI_API_KEY")
        if not resolved_api_key:
            raise ValueError("OpenAI API key not provided and not found in OPENAI_API_KEY environment variable.")

        super().__init__(api_key=resolved_api_key, default_model=default_model)
        # Initialize the OpenAI client.
        # As of openai SDK v1.0.0+, client instantiation is:
        # self.client = openai.OpenAI(api_key=self.api_key)
        # For older versions, it might be just setting openai.api_key = self.api_key
        # We'll assume a recent enough version for the new client.
        try:
            # Try to use the new OpenAI client structure (SDK v1.0.0+)
            if hasattr(openai, "OpenAI"):
                self.client = openai.OpenAI(api_key=self.api_key)
                self._is_new_sdk = True
            else: # Fallback for older openai SDK versions (pre v1.0.0)
                openai.api_key = self.api_key
                self.client = openai # The module itself acts as a client
                self._is_new_sdk = False
        except Exception as e:
             raise ImportError(f"OpenAI SDK not configured correctly or issue during initialization: {e}")


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
        Generate a chat completion using OpenAI.
        """
        effective_model = self._get_model_name(model)

        response_format_param = None
        if request_json_output:
            # Check if model is likely to support JSON mode (heuristic based on common model names)
            # Models like gpt-3.5-turbo-1106, gpt-4-1106-preview, gpt-4-turbo-preview support this.
            if "1106" in effective_model or "gpt-4" in effective_model or "turbo" in effective_model: # Broader check
                 response_format_param = {"type": "json_object"}
            else:
                # For older models, we can't guarantee JSON output via an API parameter.
                # The prompt must strongly instruct JSON output.
                print(f"Warning: OpenAIProvider - Model {effective_model} may not support guaranteed JSON mode via API params. Ensure prompt strongly requests JSON.")

        try:
            if self._is_new_sdk: # New SDK style (v1.0.0+)
                completion_params = {
                    "model": effective_model,
                    "messages": messages,
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                    **kwargs
                }
                if response_format_param:
                    completion_params["response_format"] = response_format_param

                completion = self.client.chat.completions.create(**completion_params)
                content = completion.choices[0].message.content
            else: # Attempt older SDK style (pre v1.0.0)
                # Note: response_format is not available in older SDKs.
                if response_format_param:
                     print(f"Warning: OpenAIProvider - response_format parameter ignored due to older SDK structure.")

                # Remove response_format if present in kwargs for older SDK
                kwargs.pop("response_format", None)

                completion = self.client.ChatCompletion.create( # type: ignore # openai module acts as client
                    model=effective_model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    **kwargs
                )
                content = completion.choices[0].message['content'] # type: ignore

            if request_json_output and response_format_param: # If JSON mode was explicitly set via param
                try:
                    json.loads(content if content else "") # Handle content being None
                except json.JSONDecodeError as e:
                    raise ValueError(f"OpenAIProvider: Model {effective_model} was set to JSON mode but did not return valid JSON. Error: {e}. Response: '{content}'")
            elif request_json_output: # JSON requested but not via param (best effort via prompt)
                try:
                    json.loads(content if content else "")
                except json.JSONDecodeError:
                    # This is a warning because we couldn't enforce JSON mode via API.
                    print(f"Warning: OpenAIProvider received non-JSON response when JSON was requested (best-effort via prompt) for model {effective_model}. Response: '{content[:100]}...'")

            return content if content else ""
        except openai.APIError as e: # More specific OpenAI error
            raise Exception(f"OpenAI API Error: {e}") from e
        except Exception as e:
            raise Exception(f"Error during OpenAI chat completion with model {effective_model}: {type(e).__name__} - {e}")
