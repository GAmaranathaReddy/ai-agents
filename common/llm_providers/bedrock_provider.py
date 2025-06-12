import boto3
import json
import os
from .base_llm_provider import BaseLLMProvider
from typing import List, Dict, Any, Optional

class BedrockProvider(BaseLLMProvider):
    """
    LLM provider for interacting with models via AWS Bedrock.
    Handles different request/response structures for various model providers on Bedrock.
    """

    def __init__(self,
                 default_model: Optional[str] = "anthropic.claude-3-sonnet-20240229-v1:0", # A good default that supports messages API
                 aws_region_name: Optional[str] = None,
                 aws_access_key_id: Optional[str] = None,
                 aws_secret_access_key: Optional[str] = None,
                 aws_session_token: Optional[str] = None):
        """
        Initialize the Bedrock provider.
        Args:
            default_model: Default Bedrock model ID (e.g., "anthropic.claude-3-sonnet-20240229-v1:0", "meta.llama3-70b-instruct-v1:0").
            aws_region_name: AWS region for Bedrock. If None, uses default from environment/config.
            aws_access_key_id: AWS access key ID (for explicit credentials).
            aws_secret_access_key: AWS secret access key (for explicit credentials).
            aws_session_token: AWS session token (for explicit credentials).
        """
        # Bedrock uses AWS SDK's built-in auth; api_key in superclass is not directly used for boto3 client.
        super().__init__(default_model=default_model)

        session_kwargs = {}
        if aws_access_key_id and aws_secret_access_key: # Both key and secret must be present
            session_kwargs['aws_access_key_id'] = aws_access_key_id
            session_kwargs['aws_secret_access_key'] = aws_secret_access_key
        if aws_session_token: # Often used with temporary credentials
            session_kwargs['aws_session_token'] = aws_session_token

        # Determine region
        effective_region = aws_region_name
        if not effective_region:
            effective_region = os.environ.get("AWS_BEDROCK_REGION") # Specific env var
        if not effective_region:
            effective_region = os.environ.get("AWS_REGION")
        if not effective_region:
            effective_region = os.environ.get("AWS_DEFAULT_REGION")

        # Boto3 session can also get region from ~/.aws/config if not provided.
        # If still no region, Boto3 will raise an error later if needed by the service.
        if effective_region:
             session_kwargs['region_name'] = effective_region

        try:
            session = boto3.Session(**session_kwargs)
            # If region_name wasn't in session_kwargs for client, ensure it's passed if known
            client_region_name = effective_region if effective_region else session.region_name

            if not client_region_name: # Last check for region before creating client
                 raise ValueError("AWS region for Bedrock not specified via parameter, standard AWS environment variables (AWS_REGION, AWS_DEFAULT_REGION), or AWS_BEDROCK_REGION.")

            self.bedrock_runtime = session.client(service_name='bedrock-runtime', region_name=client_region_name)
        except Exception as e:
            raise ConnectionError(f"Failed to initialize Boto3 session or Bedrock client. Ensure AWS credentials and region are configured. Error: {e}")


    def _construct_body_and_params(self, model_id: str, messages: List[Dict[str, str]],
                                   temperature: float, max_tokens: int, request_json_output: bool) -> Dict[str, Any]:
        """
        Constructs the request body and other parameters (like accept, contentType)
        based on the Bedrock model ID.
        """
        provider = model_id.split('.')[0].lower()
        body_params: Dict[str, Any] = {}
        request_params = {
            "modelId": model_id,
            "accept": "application/json",
            "contentType": "application/json"
        }

        # Standardize messages: filter out empty content, ensure roles are user/assistant (or system if supported)
        processed_messages = []
        system_prompt_parts = []
        for msg in messages:
            role = msg.get("role", "user").lower()
            content = msg.get("content", "").strip()
            if not content:
                continue
            if role == "system":
                system_prompt_parts.append(content)
            else:
                processed_messages.append({"role": role, "content": content})

        system_prompt = "\n".join(system_prompt_parts) if system_prompt_parts else None

        # Add JSON instruction if requested (prompt engineering for models that support it)
        if request_json_output:
            if processed_messages and processed_messages[-1]["role"] == "user":
                processed_messages[-1]["content"] += "\n\nIMPORTANT: Respond strictly in valid JSON format only. Do not include any explanatory text or markdown formatting before or after the JSON object."
            elif system_prompt: # Try adding to system prompt if last message not user, or no messages yet (though unlikely for chat)
                 system_prompt += "\n\nIMPORTANT: Respond strictly in valid JSON format only. Do not include any explanatory text or markdown formatting before or after the JSON object."
            else: # Fallback: create a new system message (might not be ideal for all models)
                system_prompt = "IMPORTANT: Respond strictly in valid JSON format only. Do not include any explanatory text or markdown formatting before or after the JSON object."
                print(f"Warning: BedrockProvider ({model_id}) - Had to inject JSON instruction as a new system prompt. This might affect model behavior.")


        if provider == "anthropic": # Claude models (e.g., Claude 3 Sonnet/Opus/Haiku, Claude 2.1)
            # Claude 3 models use the messages API with a top-level system prompt.
            # Older Claude models use a single text prompt with \n\nHuman: and \n\nAssistant: turns.
            if "claude-3" in model_id:
                body_params = {
                    "anthropic_version": "bedrock-2023-05-31", # Required for Claude 3
                    "max_tokens": max_tokens,
                    "temperature": temperature,
                    "messages": processed_messages # Already filtered to user/assistant
                }
                if system_prompt:
                    body_params["system"] = system_prompt
            else: # Older Claude (e.g., v2, v2.1) - single prompt construction
                claude_prompt = ""
                if system_prompt: claude_prompt += f"{system_prompt}\n\n" # Attempt to use system prompt
                for msg in processed_messages:
                    role_prefix = "Human" if msg['role'] == 'user' else "Assistant"
                    claude_prompt += f"\n\n{role_prefix}: {msg['content']}"
                claude_prompt += "\n\nAssistant:" # Crucial for Claude to start generation
                body_params = {
                    "prompt": claude_prompt,
                    "max_tokens_to_sample": max_tokens,
                    "temperature": temperature,
                }

        elif provider == "meta": # Llama models (e.g., Llama 2, Llama 3)
            # Llama 3 uses a messages format; Llama 2 typically uses a formatted prompt string.
            # Bedrock's Llama 3 instruct models support messages API.
            # For Llama 2 Chat on Bedrock, it might be better to format as a single prompt string.
            # This example prioritizes messages API for newer Llama models.
            # Note: Llama models on Bedrock might not use a top-level 'system' key in the body.
            # System prompt is often prepended to the messages list if needed.
            final_messages_for_llama = []
            if system_prompt:
                final_messages_for_llama.append({"role": "system", "content": system_prompt})
            final_messages_for_llama.extend(processed_messages)

            # Llama 3 specific body structure
            if "llama3" in model_id.lower() or "llama-3" in model_id.lower():
                 body_params = {
                    "messages": final_messages_for_llama,
                    "max_gen_len": max_tokens,
                    "temperature": temperature,
                    # "top_p": ...
                 }
            else: # Llama 2 (and potentially other Llama variants if they don't take messages)
                # Constructing a single prompt string for Llama 2 Chat
                # This is a simplified approach. Correct Llama 2 chat formatting is more complex.
                # e.g. <s>[INST] <<SYS>>{system_prompt}<</SYS>> {user_msg_1}[/INST] {model_msg_1}</s><s>[INST]...
                # For simplicity, just using the last user message combined with system prompt.
                llama2_prompt = ""
                if system_prompt: llama2_prompt += f"[INST] <<SYS>>\n{system_prompt}\n<</SYS>>\n\n"

                # Build the prompt from history, ending with the current user message
                temp_prompt_parts = []
                for msg in final_messages_for_llama: # final_messages already has system (if any) + user/assistant
                    if msg["role"] == "user":
                        temp_prompt_parts.append(f"{msg['content']} [/INST]")
                    elif msg["role"] == "assistant": # Llama 2 expects model output after [/INST]
                        temp_prompt_parts.append(f"{msg['content']} </s><s>[INST]") # Start new turn if assistant spoke

                # Remove trailing </s><s>[INST] if an assistant was the last one to speak.
                # The final prompt should end with the last user message and [/INST]
                llama2_prompt += " ".join(temp_prompt_parts)
                if not llama2_prompt.strip().endswith("[/INST]"): # Ensure it ends correctly for user turn
                    if llama2_prompt.strip().endswith("</s><s>[INST]"):
                        llama2_prompt = llama2_prompt.strip()[:-len("</s><s>[INST]")].strip()
                    # If only system prompt, add user's last message
                    if not processed_messages or processed_messages[-1]['role'] != 'user':
                         raise ValueError("BedrockProvider (Llama 2): Last message must be from user for this simplified prompt construction.")

                body_params = {
                    "prompt": llama2_prompt.strip(),
                    "max_gen_len": max_tokens,
                    "temperature": temperature,
                }

        elif provider == "amazon": # Titan models (e.g., Titan Text G1 - Express / Lite)
            # Titan generally takes a single inputText. System prompt needs to be part of this.
            titan_prompt = ""
            if system_prompt: titan_prompt += f"{system_prompt}\n\n"
            # Simplified: concatenate user/assistant turns into the inputText.
            # This might not be optimal for multi-turn chat with Titan.
            for msg in processed_messages:
                titan_prompt += f"{msg['role']}: {msg['content']}\n"
            titan_prompt += "assistant:" # To prompt the model for its turn

            body_params = {
                "inputText": titan_prompt,
                "textGenerationConfig": {
                    "maxTokenCount": max_tokens,
                    "temperature": temperature,
                }
            }

        elif provider == "cohere": # Cohere models (e.g., Command R, Command R+)
            # Cohere uses 'chat_history' and 'message'. System prompt is 'preamble'.
            # The last message in `processed_messages` is the current user query.
            cohere_chat_history = []
            current_user_message = ""

            # Separate system prompt, history, and current user message
            # Cohere's 'chat_history' expects alternating user/CHATBOT roles.
            temp_history = []
            if system_prompt: # Cohere has a preamble for system-level instructions
                body_params["preamble"] = system_prompt

            for msg in processed_messages[:-1]: # All but the last message form the history
                role = "USER" if msg["role"] == "user" else "CHATBOT"
                temp_history.append({"role": role, "message": msg["content"]})

            if processed_messages: # Ensure there's at least one message
                last_msg = processed_messages[-1]
                if last_msg["role"] == "user":
                    current_user_message = last_msg["content"]
                else: # Last message is not user, this is unexpected for typical chat flow
                    raise ValueError("BedrockProvider (Cohere): Last message in 'messages' list must be from 'user'.")
            else:
                raise ValueError("BedrockProvider (Cohere): 'messages' list cannot be empty.")

            body_params.update({
                "message": current_user_message,
                "chat_history": temp_history,
                "max_tokens": max_tokens,
                "temperature": temperature,
                # "p": ..., "k": ... (for top_p, top_k)
            })
            # Cohere does not have a direct JSON mode parameter. Relies on prompt engineering.
            if request_json_output:
                body_params["message"] += "\n\nIMPORTANT: Respond strictly in valid JSON format only. Do not include any explanatory text or markdown formatting before or after the JSON object."
                print(f"Warning: BedrockProvider (Cohere) - JSON output relies on prompt engineering. Ensure your prompt requests JSON.")

        else:
            raise ValueError(f"BedrockProvider: Model provider '{provider}' from model_id '{model_id}' is not explicitly supported by this provider's body construction logic.")

        request_params["body"] = json.dumps(body_params)
        return request_params


    def _parse_response_body(self, model_id: str, response_body_bytes: bytes) -> str:
        """
        Parses the response body bytes based on the Bedrock model ID.
        """
        provider = model_id.split('.')[0].lower()
        response_data = json.loads(response_body_bytes.decode('utf-8'))

        if provider == "anthropic": # Claude
            if "content" in response_data and isinstance(response_data["content"], list) and response_data["content"]:
                # Assuming the first content block of type 'text' is the main response for Claude 3
                for block in response_data["content"]:
                    if block.get("type") == "text":
                        return block.get("text", "")
                return "" # Should not happen if text block exists
            return response_data.get("completion", "") # For older Claude

        elif provider == "meta": # Llama
            if "generation" in response_data: # Llama 3 on Bedrock
                return response_data["generation"]
            # Fallback for Llama 2 or other structures if any (this might need adjustment based on exact model response)
            # The example `response_data.get("outputs", [{}])[0].get("text", "")` was very specific.
            # A more general Llama 2 response on Bedrock might be `response_data.get("completion")`
            return response_data.get("completion", "")

        elif provider == "amazon": # Titan
            # Titan Text G1 models
            if "results" in response_data and isinstance(response_data["results"], list) and response_data["results"]:
                return response_data["results"][0].get("outputText", "")
            return response_data.get("outputText", "") # Some Amazon Titan models might have it top-level

        elif provider == "cohere": # Cohere
            # Command R, R+
            if "text" in response_data:
                return response_data["text"]
            # Cohere might also have 'chat_history' in response, but 'text' is the direct reply.
            # Check for 'tool_calls' if using tools with Cohere in future.
            return "" # Fallback if 'text' is not found

        else:
            raise ValueError(f"BedrockProvider: Model provider '{provider}' from model_id '{model_id}' is not explicitly supported by this provider's response parsing logic.")


    def chat(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2048, # Increased default for potentially longer outputs
        request_json_output: bool = False,
        **kwargs: Any # For other invoke_model params like guardrailIdentifier
    ) -> str:
        """
        Generate a chat completion using AWS Bedrock.
        """
        effective_model_id = self._get_model_name(model)

        # _construct_body_and_params now returns the full request dict for invoke_model
        request_params = self._construct_body_and_params(
            effective_model_id, messages, temperature, max_tokens, request_json_output
        )
        # Merge additional kwargs for invoke_model itself (e.g. guardrail config)
        # Be careful not to overwrite modelId, body, accept, contentType
        invoke_kwargs = {**request_params, **kwargs}


        try:
            # print(f"[BedrockProvider DEBUG] Invoking model with: {invoke_kwargs}")
            response = self.bedrock_runtime.invoke_model(**invoke_kwargs)

            response_content_str = self._parse_response_body(effective_model_id, response.get('body').read())

            # Best-effort JSON validation if requested via prompt engineering
            if request_json_output:
                try:
                    json.loads(response_content_str)
                except json.JSONDecodeError as e_json:
                   print(f"Warning: BedrockProvider received non-JSON response when JSON was requested (best-effort prompt instruction) for model {effective_model_id}. Content snippet: {response_content_str[:100]}... Error: {e_json}")

            return response_content_str

        except boto3.exceptions.Boto3Error as e_boto: # Catch Boto3 specific errors
            raise ConnectionError(f"AWS Boto3 error during Bedrock chat completion with model {effective_model_id}: {e_boto}") from e_boto
        except Exception as e:
            raise Exception(f"Error during Bedrock chat completion with model {effective_model_id}: {type(e).__name__} - {e}")

```python
# common/llm_providers/__init__.py
from .base_llm_provider import BaseLLMProvider
from .ollama_provider import OllamaProvider
from .openai_provider import OpenAIProvider
from .gemini_provider import GeminiProvider
from .bedrock_provider import BedrockProvider # Add this

__all__ = [
    "BaseLLMProvider",
    "OllamaProvider",
    "OpenAIProvider",
    "GeminiProvider",
    "BedrockProvider" # Add this
]
```
