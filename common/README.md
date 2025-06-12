# Common Utilities

This directory contains shared utilities and configurations used across multiple agent implementations.

## LLM Configuration (`llm_config.py`)

Provides a centralized way to configure and instantiate LLM providers. Key features:

- **Provider Selection:** Choose your LLM provider (Ollama, OpenAI, Gemini, AWS Bedrock) via the `LLM_PROVIDER` environment variable. Defaults to "ollama".
- **Model Specification:** Define specific models for each provider (e.g., `OLLAMA_MODEL`, `OPENAI_MODEL`).
- **API Key Management:** Uses standard environment variables for API keys (e.g., `OPENAI_API_KEY`, `GOOGLE_API_KEY`) and AWS credentials for Bedrock.
- **Easy Instantiation:** The `get_llm_provider_instance()` function returns a ready-to-use provider object based on your configuration.

Refer to the main project README for detailed environment variable names and setup.

## LLM Providers (`llm_providers/`)

Contains the abstraction layer for interacting with different Large Language Models. See the [llm_providers README](./llm_providers/README.md) for more details on the specific provider implementations.
