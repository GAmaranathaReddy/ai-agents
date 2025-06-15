# LLM Providers

This directory implements an abstraction layer for various Large Language Model (LLM) providers. The goal is to allow agents to interact with different LLMs through a common interface.

## Base Class
- **`BaseLLMProvider`**: An abstract base class defining the standard methods (e.g., `chat()`) that all specific provider implementations must adhere to.

## Implemented Providers
Currently, the following providers are implemented:

- **`OllamaProvider`**: Interacts with locally hosted Ollama models.
- **`OpenAIProvider`**: Connects to OpenAI's API (e.g., GPT-3.5, GPT-4). Requires an `OPENAI_API_KEY`.
- **`GeminiProvider`**: Connects to Google's Gemini API. Requires a `GOOGLE_API_KEY`.
- **`BedrockProvider`**: Connects to AWS Bedrock to use models like Claude, Llama, Titan, etc. Requires AWS credentials and region configuration.

Each provider handles the specific API calls, authentication, and response parsing relevant to its service. They are instantiated and managed via the [llm_config.py](../llm_config.py) system.
