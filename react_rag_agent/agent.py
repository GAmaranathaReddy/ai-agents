# agent.py
from tools import retrieve_information # Assuming tools.py is updated for ChromaDB
import ollama
import json
import re # Still useful for some fallback or simple parsing if needed

class ReActRAGAgent:
    def __init__(self, llm_model="mistral"): # Default model for reasoning and generation
        self.name = "ReAct-RAG Bot (LLM-Powered)"
        self.llm_model = llm_model
        # The explicit keyword-based retrieval triggers might become secondary
        # or integrated into the LLM's decision process.
        # For now, we'll let the LLM try to decide first.
        # self.retrieval_keywords = ["tell me about", "what is", "explain", "describe", "info on"]
        # self.direct_lookup_keywords = ["python", "java", "ai", "react", "rag", "doc1", "doc2", "doc3", "doc4", "doc5"]
        self.current_thought_process = [] # To log steps for UI

    def _log_step(self, step_description: str):
        """Helper to add steps to the current thought process."""
        self.current_thought_process.append(step_description)
        # print(f"[LOG] {step_description}") # Optional: for console debugging

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
            llm_analysis_response = ollama.chat(
                model=self.llm_model,
                messages=[{'role': 'user', 'content': analysis_prompt}],
                format='json' # Request JSON output
            )
            analysis_content = llm_analysis_response['message']['content']
            self._log_step(f"LLM Analysis raw output: {analysis_content}")
            analysis_data = json.loads(analysis_content)

            intent = analysis_data.get("intent", "direct_answer")
            search_query = analysis_data.get("search_query")
            direct_llm_answer = analysis_data.get("llm_response")
            self._log_step(f"LLM determined intent: '{intent}'")
            if search_query:
                self._log_step(f"LLM generated search query: '{search_query}'")
            if direct_llm_answer:
                 self._log_step(f"LLM provided direct answer draft: '{direct_llm_answer[:60]}...'")

        except Exception as e:
            llm_analysis_error = f"Error during LLM query analysis: {type(e).__name__} - {e}"
            self._log_step(llm_analysis_error)
            # Fallback strategy: treat as information_seeking and use original input as search query
            intent = "information_seeking"
            search_query = user_input
            self._log_step(f"Fallback: Defaulting to intent 'information_seeking' with original input as search query.")

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
                llm_synthesis_response = ollama.chat(
                    model=self.llm_model,
                    messages=[{'role': 'user', 'content': synthesis_prompt}]
                )
                final_response = llm_synthesis_response['message']['content']
                self._log_step(f"LLM Synthesis successful. Response: \"{final_response[:60]}...\"")
            except Exception as e:
                self._log_step(f"Error during LLM response synthesis: {e}")
                final_response = "I found some information, but encountered an issue trying to synthesize a final answer. You can review the retrieved data."

        elif direct_llm_answer: # From Phase 1, intent was "direct_answer"
            self._log_step("Using direct answer from LLM Phase 1.")
            final_response = direct_llm_answer
            # action_taken_for_ui remains "LLM Analysis" or gets appended if other actions occur

        else: # Fallback if no retrieval and no direct answer, or if analysis failed badly
            if llm_analysis_error:
                 self._log_step("Attempting fallback LLM response due to earlier analysis error.")
                 # Try a generic response if analysis failed
                 try:
                    fallback_response = ollama.chat(
                        model=self.llm_model,
                        messages=[{'role': 'user', 'content': f"User asked: '{user_input}'. Respond generally."}]
                    )
                    final_response = fallback_response['message']['content']
                 except Exception as e:
                    self._log_step(f"Fallback LLM call also failed: {e}")
                    final_response = f"I'm sorry, I encountered an error and cannot process your request: '{user_input}'."
            else:
                self._log_step("No information retrieved and no direct answer from LLM analysis. Providing a default response.")
                final_response = f"I'm not sure how to respond to '{user_input}'. Could you try rephrasing or asking about topics I might have in my knowledge base (like Python, Java, AI, ReAct, RAG)?"

        return {
            "thought_process": self.current_thought_process,
            "action_taken": action_taken_for_ui, # More descriptive action string
            "query_for_retrieval": search_query,
            "retrieved_info": retrieved_info,
            "final_response": final_response
        }

if __name__ == '__main__':
    # Ensure Ollama is running: `ollama serve`
    # Ensure the model is pulled: `ollama pull mistral`
    # Ensure ChromaDB is populated: `python react_rag_agent/knowledge_base_manager.py`
    agent = ReActRAGAgent()

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
