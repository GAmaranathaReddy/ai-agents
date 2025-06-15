import os
from typing import Optional, Dict, Any
from common.llm_providers import (
    BaseLLMProvider,
    OllamaProvider,
    OpenAIProvider,
    GeminiProvider,
    BedrockProvider
)

# Environment variable names
ENV_LLM_PROVIDER = "LLM_PROVIDER"
ENV_OLLAMA_MODEL = "OLLAMA_MODEL"
ENV_OLLAMA_HOST = "OLLAMA_HOST" # Optional
ENV_OPENAI_MODEL = "OPENAI_MODEL"
ENV_OPENAI_API_KEY = "OPENAI_API_KEY" # Provider also checks this
ENV_GEMINI_MODEL = "GEMINI_MODEL"
ENV_GOOGLE_API_KEY = "GOOGLE_API_KEY" # Provider also checks this
ENV_BEDROCK_MODEL = "BEDROCK_MODEL"
ENV_AWS_REGION = "AWS_BEDROCK_REGION" # More specific than just AWS_REGION for Bedrock client
ENV_AWS_ACCESS_KEY_ID = "AWS_ACCESS_KEY_ID" # For explicit Bedrock creds
ENV_AWS_SECRET_ACCESS_KEY = "AWS_SECRET_ACCESS_KEY" # For explicit Bedrock creds
ENV_AWS_SESSION_TOKEN = "AWS_SESSION_TOKEN" # For explicit Bedrock creds


# Default values
DEFAULT_LLM_PROVIDER = "ollama"
DEFAULT_OLLAMA_MODEL = "mistral"
DEFAULT_OPENAI_MODEL = "gpt-3.5-turbo"
DEFAULT_GEMINI_MODEL = "gemini-pro"
# Example: "anthropic.claude-3-sonnet-20240229-v1:0" or "meta.llama3-8b-instruct-v1:0"
DEFAULT_BEDROCK_MODEL = "anthropic.claude-3-sonnet-20240229-v1:0"

def get_llm_provider_config() -> Dict[str, Any]:
    """
    Reads LLM provider configuration from environment variables.
    Returns a dictionary with provider name and relevant settings.
    """
    provider_name = os.environ.get(ENV_LLM_PROVIDER, DEFAULT_LLM_PROVIDER).lower()

    config: Dict[str, Any] = {"provider_name": provider_name}

    if provider_name == "ollama":
        config["model"] = os.environ.get(ENV_OLLAMA_MODEL, DEFAULT_OLLAMA_MODEL)
        config["host"] = os.environ.get(ENV_OLLAMA_HOST) # Will be None if not set, provider handles default
    elif provider_name == "openai":
        config["model"] = os.environ.get(ENV_OPENAI_MODEL, DEFAULT_OPENAI_MODEL)
        config["api_key"] = os.environ.get(ENV_OPENAI_API_KEY) # Provider will re-check but good to pass if explicitly set
    elif provider_name == "gemini":
        config["model"] = os.environ.get(ENV_GEMINI_MODEL, DEFAULT_GEMINI_MODEL)
        config["api_key"] = os.environ.get(ENV_GOOGLE_API_KEY)
    elif provider_name == "bedrock":
        config["model"] = os.environ.get(ENV_BEDROCK_MODEL, DEFAULT_BEDROCK_MODEL)
        config["aws_region_name"] = os.environ.get(ENV_AWS_REGION)
        config["aws_access_key_id"] = os.environ.get(ENV_AWS_ACCESS_KEY_ID)
        config["aws_secret_access_key"] = os.environ.get(ENV_AWS_SECRET_ACCESS_KEY)
        config["aws_session_token"] = os.environ.get(ENV_AWS_SESSION_TOKEN)
    else:
        supported_providers = ["ollama", "openai", "gemini", "bedrock"]
        raise ValueError(f"Unsupported LLM_PROVIDER: '{provider_name}'. Supported providers are: {', '.join(supported_providers)}.")

    return config

def get_llm_provider_instance() -> BaseLLMProvider:
    """
    Instantiates and returns the configured LLM provider based on environment variables.
    """
    config = get_llm_provider_config()
    provider_name = config["provider_name"]
    model = config.get("model") # Model might not be needed by all providers in config dict if they have own defaults

    # print(f"[llm_config DEBUG] Instantiating provider: {provider_name} with model: {model}")

    if provider_name == "ollama":
        return OllamaProvider(default_model=model, host=config.get("host"))
    elif provider_name == "openai":
        # OpenAIProvider's __init__ will raise ValueError if API key is missing
        return OpenAIProvider(default_model=model, api_key=config.get("api_key"))
    elif provider_name == "gemini":
        # GeminiProvider's __init__ will raise ValueError if API key is missing
        return GeminiProvider(default_model=model, api_key=config.get("api_key"))
    elif provider_name == "bedrock":
        # BedrockProvider's __init__ will raise ValueError if region is missing and not in env
        return BedrockProvider(
            default_model=model,
            aws_region_name=config.get("aws_region_name"),
            aws_access_key_id=config.get("aws_access_key_id"),
            aws_secret_access_key=config.get("aws_secret_access_key"),
            aws_session_token=config.get("aws_session_token")
        )

    # This line should ideally not be reached due to validation in get_llm_provider_config
    # but as a safeguard:
    raise ValueError(f"Failed to instantiate provider for unknown or unhandled provider name: '{provider_name}'")

if __name__ == "__main__":
    # Example usage and testing
    print("--- LLM Configuration Test ---")
    print(f"Reading LLM provider configuration from environment variables (or defaults)...")

    # You can temporarily set environment variables here for testing, e.g.:
    # os.environ[ENV_LLM_PROVIDER] = "openai"
    # os.environ[ENV_OPENAI_API_KEY] = "your_fake_key_for_testing_config_loading"
    # os.environ[ENV_OPENAI_MODEL] = "gpt-4-test"

    try:
        active_config = get_llm_provider_config()
        print("\n--- Active Configuration Retrieved ---")
        for key, value in active_config.items():
            # Mask sensitive keys for printing
            if key in [ENV_OPENAI_API_KEY, ENV_GOOGLE_API_KEY, ENV_AWS_SECRET_ACCESS_KEY, "api_key"]:
                print(f"  {key}: {'********' if value else 'Not set/Using environment default'}")
            else:
                print(f"  {key}: {value if value else 'Not set/Using default'}")

        print("\n--- Attempting to Instantiate Provider ---")
        provider_instance = get_llm_provider_instance()
        print(f"Successfully instantiated provider: {type(provider_instance).__name__}")
        print(f"Default model for this provider instance: {provider_instance.default_model}")

        if isinstance(provider_instance, OllamaProvider):
             print("Ollama specific: Ensure Ollama server is running and model is pulled for actual use.")
        elif isinstance(provider_instance, OpenAIProvider):
             print(f"OpenAI specific: Ensure OPENAI_API_KEY is valid for model '{provider_instance.default_model}' for actual use.")
        elif isinstance(provider_instance, GeminiProvider):
             print(f"Gemini specific: Ensure GOOGLE_API_KEY is valid for model '{provider_instance.default_model}' for actual use.")
        elif isinstance(provider_instance, BedrockProvider):
             print(f"Bedrock specific: Ensure AWS credentials and region are correctly configured for model '{provider_instance.default_model}' for actual use.")

    except ValueError as ve:
        print(f"\nCONFIG_ERROR: {ve}")
    except ConnectionError as ce:
        print(f"\nCONNECTION_ERROR: {ce}")
    except Exception as e:
        print(f"\nUNEXPECTED_ERROR during configuration test: {type(e).__name__} - {e}")

    # Example of unsetting a temporarily set env var for testing
    # if ENV_LLM_PROVIDER in os.environ:
    #     del os.environ[ENV_LLM_PROVIDER]
