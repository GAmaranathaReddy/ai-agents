# agent.py
from .tools import retrieve_information # Corrected import path, assuming tools.py is in the same dir
from common.llm_providers.client import get_llm_client, SUPPORTED_PROVIDERS, DEFAULT_PROVIDER
from typing import List, Dict, Optional # For type hinting
import json
import re

class ReActRAGAgent:
    def __init__(self, provider_name: Optional[str] = None, model_name: Optional[str] = None, **provider_kwargs):
        """
        Initializes the ReActRAGAgent using a specified provider and model
        via the common LLM client factory.

        Args:
            provider_name (str, optional): Name of the LLM provider.
            model_name (str, optional): The specific model name to use.
                                        Consider models good at JSON output and reasoning.
            **provider_kwargs: Additional args for the provider's constructor.
        """
        try:
            self.llm_client = get_llm_client(provider_name, **provider_kwargs)
            self.actual_provider_name = self.llm_client.__class__.__name__.replace("Provider", "")
        except Exception as e:
            print(f"FATAL: Error initializing LLM client for ReActRAGAgent provider '{provider_name or DEFAULT_PROVIDER}': {e}")
            raise RuntimeError(f"Failed to initialize LLM client for ReActRAGAgent: {e}") from e

        # Determine model: Use provided, then provider's default, then agent's provider-specific default
        if model_name:
            self.llm_model = model_name
        elif hasattr(self.llm_client, 'default_model') and self.llm_client.default_model:
            self.llm_model = self.llm_client.default_model
        else: # Fallback to agent's own defaults for specific providers if needed
            if self.actual_provider_name.lower() == "ollama":
                self.llm_model = "mistral"
            elif self.actual_provider_name.lower() == "openai":
                self.llm_model = "gpt-3.5-turbo-1106" # Newer version, better at JSON
            elif self.actual_provider_name.lower() == "gemini":
                self.llm_model = "gemini-pro"
            elif self.actual_provider_name.lower() == "bedrock":
                self.llm_model = "anthropic.claude-3-sonnet-20240229-v1:0"
            else:
                raise ValueError(f"No model_name specified and could not determine a default for ReActRAGAgent with provider '{self.actual_provider_name}'.")

        self.name = f"ReAct-RAG Agent ({self.actual_provider_name}/{self.llm_model})"
        self.current_thought_process = []

    def _log_step(self, step_description: str):
        self.current_thought_process.append(step_description)

    def reason_and_act(self, user_input: str) -> dict:
        """
        Implements an LLM-driven ReAct (Reason, Act) and RAG (Retrieval Augmented Generation) flow.
        """
        self.current_thought_process = [] # Reset for each request
        self._log_step(f"Received user input: \"{user_input}\"")

        # --- Phase 1: Query Analysis & Search Query Formulation (LLM Call 1) ---
        self._log_step("Phase 1: Analyzing query with LLM...")
        analysis_prompt = f"""Analyze the following user query: "{user_input}"
        Determine the user's intent and how to best respond.
        Possible intents are:
        1. "information_seeking": The user is looking for specific information that might be in a knowledge base.
        2. "direct_answer": The query is a general question, greeting, or statement that the LLM can attempt to answer directly.

        If the intent is "information_seeking":
          - Extract or generate a concise search query suitable for a vector database lookup.
          - The search query should capture the core information need.
          - Respond in JSON format: {{"intent": "information_seeking", "search_query": "your_generated_search_query"}}

        If the intent is "direct_answer":
          - Provide a direct, helpful answer to the query if possible.
          - Respond in JSON format: {{"intent": "direct_answer", "llm_response": "your_direct_answer"}}

        If unsure, default to "direct_answer" and attempt a response.
        Only provide the JSON response.
        """

        intent = "direct_answer" # Default intent
        search_query = None
        direct_llm_answer = None
        llm_analysis_error = None

        try:
            analysis_content_str = self.llm_client.chat( # Use new client and pass model
                model=self.llm_model,
                messages=[{'role': 'user', 'content': analysis_prompt}],
                format_json=True
            )
            self._log_step(f"LLM Analysis raw output: {analysis_content_str}")
            analysis_data = json.loads(analysis_content_str)

            intent = analysis_data.get("intent", "direct_answer")
            search_query = analysis_data.get("search_query")
            direct_llm_answer = analysis_data.get("llm_response")
            self._log_step(f"LLM determined intent: '{intent}'")
            if search_query:
                self._log_step(f"LLM generated search query: '{search_query}'")
            if direct_llm_answer:
                 self._log_step(f"LLM provided direct answer draft: '{direct_llm_answer[:60]}...'")

        except json.JSONDecodeError as e:
            llm_analysis_error = f"Error parsing JSON from LLM query analysis ({self.actual_provider_name}/{self.llm_model}): {type(e).__name__} - {e}. Raw: {analysis_content_str}"
            self._log_step(llm_analysis_error)
            intent = "information_seeking"; search_query = user_input; direct_llm_answer = None # Fallback
            self._log_step(f"Fallback due to JSON error: Defaulting to intent 'information_seeking' with original input as search query.")
        except Exception as e: # Catch other LLM call errors
            llm_analysis_error = f"Error during LLM query analysis ({self.actual_provider_name}/{self.llm_model}): {type(e).__name__} - {e}"
            self._log_step(llm_analysis_error)
            intent = "information_seeking"; search_query = user_input; direct_llm_answer = None # Fallback
            self._log_step(f"Fallback due to LLM error: Defaulting to intent 'information_seeking' with original input as search query.")

        # --- Phase 2: Retrieval (if intent is "information_seeking") ---
        retrieved_info = None
        action_taken_for_ui = "LLM Analysis" # Initial action

        if intent == "information_seeking" and search_query:
            self._log_step(f"Phase 2: Retrieving information from ChromaDB with query: '{search_query}'")
            action_taken_for_ui = f"LLM Analysis -> ChromaDB Retrieval (query: '{search_query}')"
            try:
                retrieved_info = retrieve_information(search_query, n_results=2) # Retrieve top 2 results
                if "No relevant document found" in retrieved_info:
                    self._log_step(f"Observation: Retrieval from ChromaDB found no document for '{search_query}'.")
                    retrieved_info = None # Standardize "not found" to None
                else:
                    self._log_step(f"Observation: Retrieval from ChromaDB returned: \"{retrieved_info[:100]}...\"")
            except Exception as e:
                self._log_step(f"Error during ChromaDB retrieval: {e}")
                retrieved_info = None
        elif intent == "information_seeking" and not search_query:
            self._log_step("Phase 2: Skipped retrieval because LLM analysis did not provide a search query, though intent was information_seeking.")


        # --- Phase 3: Response Synthesis (LLM Call 2 or direct answer) ---
        self._log_step("Phase 3: Synthesizing final response...")
        final_response = None

        if retrieved_info:
            action_taken_for_ui += " -> LLM Synthesis"
            self._log_step("Synthesizing response using retrieved context with LLM...")
            synthesis_prompt = f"""The user asked: "{user_input}"
            I found the following information from a knowledge base:
            --- Start of Retrieved Context ---
            {retrieved_info}
            --- End of Retrieved Context ---
            Based on this information and the user's original query, please formulate a comprehensive and helpful answer.
            If the retrieved context seems irrelevant, you can state that you found some information but it might not directly answer the query, then try to answer generally if possible.
            """
            try:
            try:
                final_response = self.llm_client.chat( # Use new client and pass model
                    model=self.llm_model,
                    messages=[{'role': 'user', 'content': synthesis_prompt}],
                    format_json=False # Expecting natural language response
                )
                self._log_step(f"LLM Synthesis successful. Response: \"{final_response[:60]}...\"")
            except Exception as e:
                self._log_step(f"Error during LLM response synthesis ({self.actual_provider_name}/{self.llm_model}): {e}")
                final_response = "I found some information, but encountered an issue trying to synthesize a final answer. You can review the retrieved data."

        elif direct_llm_answer: # From Phase 1, intent was "direct_answer"
            self._log_step("Using direct answer from LLM Phase 1.")
            final_response = direct_llm_answer

        else: # Fallback if no retrieval and no direct answer, or if analysis failed badly
            if llm_analysis_error: # If analysis failed, try a general response
                 self._log_step("Attempting fallback LLM response due to earlier analysis error.")
                 try:
                    final_response = self.llm_client.chat( # Use new client and pass model
                        model=self.llm_model,
                        messages=[{'role': 'user', 'content': f"The user asked: '{user_input}'. Please provide a general response as there was an issue processing it further."}],
                        format_json=False
                    )
                 except Exception as e:
                    self._log_step(f"Fallback LLM call also failed ({self.actual_provider_name}/{self.llm_model}): {e}")
                    final_response = f"I'm sorry, I encountered an error and cannot process your request: '{user_input}'."
            else: # No retrieval, no direct_llm_answer, and no analysis error (e.g. intent was info_seeking but no search_query)
                self._log_step("No information retrieved and no direct answer from LLM analysis. Providing a default response.")
                final_response = f"I'm not sure how to respond to '{user_input}'. Could you try rephrasing?"

        return {
            "thought_process": self.current_thought_process,
            "action_taken": action_taken_for_ui, # More descriptive action string
            "query_for_retrieval": search_query,
            "retrieved_info": retrieved_info,
            "final_response": final_response
        }

if __name__ == '__main__':
    # Ensure your chosen LLM provider is configured via environment variables
    # (e.g., LLM_PROVIDER, OLLAMA_MODEL, OPENAI_API_KEY, etc.)
    # and that any necessary services (like Ollama server) are running.
    # Also ensure ChromaDB is populated: `python react_rag_agent/knowledge_base_manager.py`

    print("Instantiating ReActRAGAgent (will use configured LLM provider)...")
    try:
        agent = ReActRAGAgent()
        print(f"Agent initialized: {agent.name}")

    test_inputs = [
        "hello",
        "tell me about python",
        "what is AI?", # Note: case difference, and question mark
        "explain RAG",
        "describe Java",
        "info on react",
        "python", # Direct lookup
        "doc1",   # Direct ID lookup
        "tell me about", # Incomplete query
        "gibberish query",
        "Can you tell me about the Python programming language?", # Embedded keyword
        "What is the definition of artificial intelligence, commonly known as AI?" # Embedded keyword
    ]

    for text_input in test_inputs:
        results = agent.reason_and_act(text_input)
        print(f"User: {text_input}")
        print(f"  Thoughts: {results['thought_process']}")
        if results['action_taken']:
            print(f"  Action: {results['action_taken']}")
            print(f"  Query for Retrieval: {results['query_for_retrieval']}")
        if results['retrieved_info']:
            print(f"  Retrieved Info (Snippet): {results['retrieved_info'][:60]}...")
        print(f"  Final Response: {results['final_response']}")
        print("-" * 30 + "\n")
