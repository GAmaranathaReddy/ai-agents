import google.generativeai as genai
import os
from .base_llm_provider import BaseLLMProvider
from typing import List, Dict, Any, Optional
import json

class GeminiProvider(BaseLLMProvider):
    """
    LLM provider for interacting with Google's Gemini models.
    """

    def __init__(self, api_key: Optional[str] = None, default_model: Optional[str] = "gemini-pro"):
        """
        Initialize the Gemini provider.
        Args:
            api_key: Google API key. If None, attempts to load from GOOGLE_API_KEY env var.
            default_model: Default Gemini model to use (e.g., "gemini-pro", "gemini-1.5-pro-latest").
        """
        resolved_api_key = api_key if api_key else os.environ.get("GOOGLE_API_KEY")
        if not resolved_api_key:
            raise ValueError("Google API key not provided and not found in GOOGLE_API_KEY environment variable.")

        super().__init__(api_key=resolved_api_key, default_model=default_model)
        try:
            genai.configure(api_key=self.api_key)
        except Exception as e:
            raise ConnectionError(f"Failed to configure Gemini client. Ensure GOOGLE_API_KEY is valid. Error: {e}")
        # Client is implicitly configured by genai.configure

    def _convert_messages_to_gemini_format(self, messages: List[Dict[str, str]]) -> List[Dict[str, Any]]:
        """
        Converts a list of standard message dictionaries to Gemini's format.
        Gemini expects 'parts' and alternates roles, ensuring 'user' and 'model' sequence.
        The last message should typically be from a 'user'.
        This is a simplified converter; robust handling might require managing history to ensure strict alternation.
        """
        gemini_history = []
        # Ensure roles are 'user' or 'model'
        for i, message in enumerate(messages):
            role = message.get("role", "user").lower()
            content = message.get("content", "")

            if role == "assistant" or role == "system": # System role might need special handling or be prepended
                role = "model"

            # Basic role alternation check: if current role is same as last, it might be problematic for Gemini
            # However, Gemini's `generate_content` is somewhat flexible with a list of contents.
            # The primary concern is that `user` and `model` roles should alternate.
            # If the last message was 'model', and current is 'model', this is an issue.
            # If last was 'user' and current is 'user', this is also an issue.
            # This simplified version just maps them. More complex logic might be needed for strict SDKs.
            gemini_history.append({"role": role, "parts": [content]})
        return gemini_history

    def chat(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.7, # Gemini's default is often 0.9 or 1.0 for some models
        max_tokens: Optional[int] = None, # Gemini calls this max_output_tokens
        request_json_output: bool = False,
        **kwargs: Any # For other params like top_p, top_k
    ) -> str:
        """
        Generate a chat completion using Gemini.
        """
        effective_model = self._get_model_name(model)

        try:
            generative_model = genai.GenerativeModel(effective_model)
        except Exception as e:
            raise ValueError(f"Failed to initialize Gemini GenerativeModel with model '{effective_model}'. Error: {e}")

        # Construct generation_config
        generation_config_params = {"temperature": temperature}
        if max_tokens is not None:
            generation_config_params["max_output_tokens"] = max_tokens

        # Allow overriding or adding other generation_config params via kwargs
        # e.g. kwargs = {"generation_config_override": {"top_p": 0.9}}
        if "generation_config_override" in kwargs:
            generation_config_params.update(kwargs.pop("generation_config_override"))

        # Remaining kwargs can be passed to generate_content if they are valid safety_settings etc.
        # For simplicity, we'll primarily use generation_config for main params.

        generation_config = genai.types.GenerationConfig(**generation_config_params)

        if not messages:
            raise ValueError("Messages list cannot be empty for Gemini chat.")

        gemini_formatted_messages = self._convert_messages_to_gemini_format(messages)

        # If JSON output is requested, append instructions to the *last user message's content*.
        # This is a common way to instruct models when a dedicated API parameter isn't available.
        if request_json_output:
            if gemini_formatted_messages and gemini_formatted_messages[-1]['role'] == 'user':
                # Ensure 'parts' is a list and modify its first element (the text part)
                if isinstance(gemini_formatted_messages[-1]['parts'], list) and \
                   len(gemini_formatted_messages[-1]['parts']) > 0 and \
                   isinstance(gemini_formatted_messages[-1]['parts'][0], str):
                    gemini_formatted_messages[-1]['parts'][0] += "\nIMPORTANT: Respond strictly in JSON format only. Do not include any explanatory text before or after the JSON object."
                else: # Fallback if parts structure is not as expected (e.g. not a list or not string)
                    # This might happen if parts contain non-string data, which is not typical for this message structure
                    gemini_formatted_messages[-1]['parts'] = [str(gemini_formatted_messages[-1]['parts']) + "\nIMPORTANT: Respond strictly in JSON format only. Do not include any explanatory text before or after the JSON object."]

            else:
                # If the last message isn't from 'user', it's harder to inject this instruction cleanly.
                # We could add a new user message, but that changes the conversation flow.
                # For now, we'll warn if we can't inject it as expected.
                print(f"Warning: GeminiProvider - Could not reliably inject JSON instruction. Last message role: {gemini_formatted_messages[-1]['role'] if gemini_formatted_messages else 'None'}")

        try:
            # print(f"[GeminiProvider DEBUG] Request: model={effective_model}, messages={gemini_formatted_messages}, config={generation_config}, kwargs={kwargs}")
            response = generative_model.generate_content(
                contents=gemini_formatted_messages,
                generation_config=generation_config,
                **kwargs # Pass other valid arguments like safety_settings
            )

            if not response.candidates:
                 if response.prompt_feedback and response.prompt_feedback.block_reason:
                     raise ValueError(f"Gemini API call failed due to prompt blocking: {response.prompt_feedback.block_reason.name} - {response.prompt_feedback.block_reason_message if hasattr(response.prompt_feedback, 'block_reason_message') else 'No message provided.'}")
                 else: # General failure without specific block reason
                     raise ValueError("Gemini API call failed: No candidates returned and no specific block reason. Check safety settings or prompt content.")

            content = response.text

            if request_json_output:
                try:
                    json.loads(content)
                except json.JSONDecodeError as e_json:
                    # LLM failed to produce valid JSON despite instruction.
                    print(f"Warning: GeminiProvider received non-JSON response when JSON was requested (best-effort prompt instruction) for model {effective_model}. Content snippet: {content[:100]}... Error: {e_json}")
                    # Depending on strictness, one might raise an error here or return the non-JSON string.
                    # For now, returning the string as is, with a warning printed.

            return content
        except genai.types.BlockedPromptException as e_blocked: # More specific exception
            raise ValueError(f"Gemini API call failed due to prompt blocking: {e_blocked}") from e_blocked
        except Exception as e:
            raise Exception(f"Error during Gemini chat completion with model {effective_model}: {type(e).__name__} - {e}")
