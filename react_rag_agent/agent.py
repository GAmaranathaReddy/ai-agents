# agent.py
from tools import retrieve_information
import re

class ReActRAGAgent:
    def __init__(self):
        self.name = "ReAct-RAG Bot"
        # Keywords that trigger the retrieval action
        self.retrieval_keywords = ["tell me about", "what is", "explain", "describe", "info on"]
        # More specific keywords for direct lookup (can be document IDs or very specific terms)
        self.direct_lookup_keywords = ["python", "java", "ai", "react", "rag", "doc1", "doc2", "doc3", "doc4", "doc5"]

    def reason_and_act(self, user_input: str) -> str:
        """
        Implements the ReAct (Reason, Act) and RAG (Retrieval Augmented Generation) flow.

        1.  **Reason**: Analyzes the user input to determine if a tool (retrieval) is needed.
        2.  **Act**: If a tool is needed, it calls the tool (retrieve_information).
        3.  **Generate**: Formulates a response, augmented by the retrieved information if available.
        """
        user_input_lower = user_input.lower()
        thought_process = [] # To store the agent's "thoughts"

        # --- REASONING PHASE ---
        action_to_take = None
        query_for_retrieval = user_input # Default query is the full input

        # Check for direct lookup keywords first
        for lookup_term in self.direct_lookup_keywords:
            if lookup_term == user_input_lower: # Exact match for direct lookup
                action_to_take = "retrieve_direct"
                query_for_retrieval = lookup_term
                thought_process.append(f"Thought: User input '{user_input}' is a direct lookup term ('{lookup_term}'). Planning to retrieve.")
                break

        if not action_to_take: # If no direct lookup, check for general retrieval phrases
            for keyword_phrase in self.retrieval_keywords:
                if user_input_lower.startswith(keyword_phrase):
                    action_to_take = "retrieve_general"
                    # Extract the actual subject from the query
                    # e.g., "tell me about python" -> "python"
                    query_for_retrieval = user_input_lower.replace(keyword_phrase, "").strip()
                    if not query_for_retrieval: # e.g. user just said "tell me about"
                        thought_process.append(f"Thought: User input '{user_input}' uses retrieval phrase '{keyword_phrase}' but provided no specific topic. Cannot act.")
                        action_to_take = None # Reset action
                    else:
                        thought_process.append(f"Thought: User input '{user_input}' starts with retrieval phrase '{keyword_phrase}'. Topic: '{query_for_retrieval}'. Planning to retrieve.")
                    break

        if not action_to_take:
             # More sophisticated check: if the input contains any of the direct lookup keywords
            found_keywords_in_input = [dk for dk in self.direct_lookup_keywords if dk in user_input_lower]
            if found_keywords_in_input:
                # Heuristic: use the longest found keyword as the query focus
                query_for_retrieval = max(found_keywords_in_input, key=len)
                action_to_take = "retrieve_embedded_keyword"
                thought_process.append(f"Thought: User input '{user_input}' contains known keyword '{query_for_retrieval}'. Planning to retrieve.")


        # --- ACTING PHASE ---
        retrieved_info = None
        if action_to_take in ["retrieve_direct", "retrieve_general", "retrieve_embedded_keyword"]:
            thought_process.append(f"Action: Calling retrieve_information tool with query: '{query_for_retrieval}'.")
            retrieved_info = retrieve_information(query_for_retrieval)
            if "No relevant document found" in retrieved_info:
                thought_process.append(f"Observation: Retrieval tool found no document for '{query_for_retrieval}'.")
            else:
                thought_process.append(f"Observation: Retrieval tool returned: \"{retrieved_info[:50]}...\"")
        else:
            thought_process.append("Thought: No specific retrieval action identified. Will generate a default response.")

        # --- GENERATION PHASE (Augmented by retrieved info) ---
        final_response = ""
        if retrieved_info and "No relevant document found" not in retrieved_info:
            # RAG: Augmenting generation with retrieved information
            final_response = f"Based on available information about '{query_for_retrieval}': {retrieved_info}"
        elif action_to_take and not retrieved_info: # Tried to retrieve but got nothing specific
             final_response = f"I tried to find information about '{query_for_retrieval}', but I couldn't find anything specific in my knowledge base."
        elif "Cannot act" in " ".join(thought_process): # Specific thought indicating inability to act
            final_response = f"You asked me to '{user_input_lower}', but I need a bit more specific topic to look up. For example, 'tell me about python'."
        else:
            # Default response if no specific action or retrieval
            final_response = f"I'm {self.name}. You said: '{user_input}'. How can I help you with topics like Python, Java, AI, ReAct, or RAG?"

        # Optionally, include the thought process in the response for debugging/transparency
        # return f"Thoughts:\n- " + "\n- ".join(thought_process) + f"\n\nResponse: {final_response}"
        return final_response

if __name__ == '__main__':
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
        response = agent.reason_and_act(text_input)
        print(f"User: {text_input}")
        # For cleaner output, we're not printing thoughts here, but they are logged in the method
        # print(f"Agent Thoughts & Response:\n{response}\n" + "-"*30)
        print(f"Agent: {response}\n" + "-"*30)
