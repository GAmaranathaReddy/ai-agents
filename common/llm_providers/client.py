import os
from typing import Any # Added for **kwargs type hint
from .base import LLMProvider
from .ollama_provider import OllamaProvider
from .openai_provider import OpenAIProvider
from .gemini_provider import GeminiProvider
from .bedrock_provider import BedrockProvider

SUPPORTED_PROVIDERS = {
    "ollama": OllamaProvider,
    "openai": OpenAIProvider,
    "gemini": GeminiProvider,
    "bedrock": BedrockProvider,
}

DEFAULT_PROVIDER = "ollama" # Default to Ollama if not specified

def get_llm_client(provider_name: str = None, **kwargs: Any) -> LLMProvider:
    """
    Factory function to get an instance of an LLM provider.

    Args:
        provider_name (str, optional): The name of the provider (e.g., "ollama", "openai").
                       If None, attempts to read from LLM_PROVIDER environment variable.
                       Defaults to "ollama" if not found.
        **kwargs: Additional keyword arguments to pass to the provider's constructor
                  (e.g., api_key, default_model for OpenAI/Gemini;
                   region_name, default_model for Bedrock;
                   default_model for OllamaProvider - though Ollama model is per-call).

    Returns:
        An instance of the requested LLMProvider.

    Raises:
        ValueError: If the specified provider is not supported or if required
                    API keys/config are missing for that provider (raised from provider's __init__).
        Exception: For other unexpected initialization errors.
    """
    if provider_name is None:
        provider_name = os.getenv("LLM_PROVIDER", DEFAULT_PROVIDER).lower()
    else:
        provider_name = provider_name.lower()

    if provider_name not in SUPPORTED_PROVIDERS:
        raise ValueError(
            f"Unsupported LLM provider: '{provider_name}'. "
            f"Supported providers are: {list(SUPPORTED_PROVIDERS.keys())}"
        )

    ProviderClass = SUPPORTED_PROVIDERS[provider_name]

    try:
        # Relevant kwargs will be picked up by the respective ProviderClass constructor
        # e.g., OllamaProvider() takes no specific args in its __init__ in this design
        # OpenAIProvider(api_key=..., default_model=...)
        # GeminiProvider(api_key=..., default_model=...)
        # BedrockProvider(region_name=..., default_model=...)
        # Unused kwargs for a specific provider will be ignored if its __init__ doesn't accept them.
        return ProviderClass(**kwargs)
    except ValueError as ve: # Catch API key errors or other ValueErrors from providers' __init__
        raise ValueError(f"Error initializing {ProviderClass.__name__} for provider '{provider_name}': {ve}")
    except ConnectionError as ce: # Catch connection errors (e.g. Bedrock client init)
        raise ConnectionError(f"Connection error initializing {ProviderClass.__name__} for provider '{provider_name}': {ce}")
    except Exception as e: # Catch other potential init errors
        # It's often better to let specific exceptions from providers propagate if they are informative,
        # or wrap them consistently.
        raise Exception(f"Could not initialize {ProviderClass.__name__} for provider '{provider_name}': {type(e).__name__} - {e}")

if __name__ == '__main__':
    print("Testing LLM Client Factory...")

    # Test with default (Ollama) - assuming Ollama is running
    print("\n--- Testing with default (Ollama) ---")
    try:
        ollama_client = get_llm_client() # No provider name, should default or use LLM_PROVIDER env var
        print(f"Successfully got Ollama client: {ollama_client}")
        # Test a simple call if Ollama is running and "mistral" is pulled
        # print(ollama_client.chat(model="mistral", messages=[{"role":"user", "content":"Say hi"}]))
    except Exception as e:
        print(f"Error getting default Ollama client: {e}")

    # Test with OpenAI (requires OPENAI_API_KEY to be set in env)
    print("\n--- Testing with OpenAI ---")
    if os.getenv("OPENAI_API_KEY"):
        try:
            openai_client = get_llm_client("openai", default_model="gpt-3.5-turbo")
            print(f"Successfully got OpenAI client: {openai_client}")
            # print(openai_client.chat(messages=[{"role":"user", "content":"Briefly, what is OpenAI?"}], max_tokens=20))
        except Exception as e:
            print(f"Error getting OpenAI client: {e}")
    else:
        print("Skipping OpenAI test: OPENAI_API_KEY not set.")

    # Test with Gemini (requires GOOGLE_API_KEY to be set in env)
    print("\n--- Testing with Gemini ---")
    if os.getenv("GOOGLE_API_KEY"):
        try:
            gemini_client = get_llm_client("gemini", default_model="gemini-pro")
            print(f"Successfully got Gemini client: {gemini_client}")
            # print(gemini_client.chat(messages=[{"role":"user", "content":"What is Google Gemini?"}], max_tokens=20))
        except Exception as e:
            print(f"Error getting Gemini client: {e}")
    else:
        print("Skipping Gemini test: GOOGLE_API_KEY not set.")

    # Test with Bedrock (requires AWS credentials and region to be configured)
    print("\n--- Testing with Bedrock ---")
    try:
        # Example: Pass region_name if not default, and a specific default_model
        bedrock_client = get_llm_client("bedrock", region_name="us-east-1", default_model="anthropic.claude-3-sonnet-20240229-v1:0")
        print(f"Successfully got Bedrock client: {bedrock_client}")
        # Test call would require model access configured for the AWS credentials
        # print(bedrock_client.chat(messages=[{"role":"user", "content":"What is AWS Bedrock in one sentence?"}], max_tokens=30))
    except Exception as e:
        print(f"Error getting Bedrock client: {e} (Ensure AWS credentials/region are set up and you have model access)")

    # Test with an unsupported provider
    print("\n--- Testing with unsupported provider ---")
    try:
        unsupported_client = get_llm_client("myllm")
    except ValueError as e:
        print(f"Correctly caught error for unsupported client: {e}")
    except Exception as e:
        print(f"Unexpected error for unsupported client: {e}")

    # Test with explicit provider and kwargs
    print("\n--- Testing with explicit provider and kwargs (OpenAI) ---")
    if os.getenv("OPENAI_API_KEY"):
        try:
            openai_client_kwargs = get_llm_client(provider_name="openai", api_key="dummy_key_if_not_env_used_by_provider", default_model="gpt-4")
            # Note: OpenAIProvider uses os.getenv first if api_key is None, so dummy_key might not be used if env var is set.
            # This depends on the provider's __init__ logic.
            print(f"Successfully got OpenAI client with kwargs: {openai_client_kwargs} using model {openai_client_kwargs.default_model}")
        except Exception as e:
            print(f"Error getting OpenAI client with kwargs: {e}")
    else:
        print("Skipping OpenAI with kwargs test: OPENAI_API_KEY not set.")
