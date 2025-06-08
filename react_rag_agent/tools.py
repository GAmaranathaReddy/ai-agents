# tools.py
from knowledge_base import DOCUMENTS, STRUCTURED_DOCUMENTS

def retrieve_document_simple(query: str) -> str:
    """
    Retrieves a document from the simple DOCUMENTS dictionary based on keyword matching.

    Args:
        query (str): The user's query.

    Returns:
        str: The content of the relevant document or a "not found" message.
    """
    query_lower = query.lower()
    # Check for direct key matches first
    if query_lower in DOCUMENTS:
        return DOCUMENTS[query_lower]

    # Then check for keywords within the query
    for keyword, doc_text in DOCUMENTS.items():
        if keyword in query_lower:
            return doc_text
    return "No relevant document found in simple knowledge base."

def retrieve_document_structured(query: str) -> str:
    """
    Retrieves a document from the STRUCTURED_DOCUMENTS list based on keyword matching
    within the 'keywords' field or 'id' of each document.

    Args:
        query (str): The user's query.

    Returns:
        str: The text of the relevant document or a "not found" message.
    """
    query_lower = query.lower()

    # Check for ID match
    for doc in STRUCTURED_DOCUMENTS:
        if doc["id"] == query_lower:
            return doc["text"]

    # Check for keyword matches
    best_match_doc = None
    max_keyword_matches = 0

    for doc in STRUCTURED_DOCUMENTS:
        current_matches = 0
        for keyword in doc["keywords"]:
            if keyword in query_lower:
                current_matches +=1

        if current_matches > max_keyword_matches:
            max_keyword_matches = current_matches
            best_match_doc = doc

    if best_match_doc:
        return best_match_doc["text"]

    return "No relevant document found in structured knowledge base."


# For this agent, we will primarily use the structured retrieval for better demonstration
def retrieve_information(query: str) -> str:
    """
    Primary retrieval function for the agent.
    Currently defaults to using the structured retrieval.
    """
    # We could add logic here to choose which retrieval to use,
    # or combine results. For now, just use the structured one.
    retrieved_text = retrieve_document_structured(query)

    if "No relevant document found" in retrieved_text:
        # Fallback to simple retrieval if structured fails
        retrieved_text_simple = retrieve_document_simple(query)
        if "No relevant document found" not in retrieved_text_simple:
            return retrieved_text_simple # Return simple's finding

    return retrieved_text

if __name__ == '__main__':
    print("Testing tools.py...")

    queries = [
        "python",
        "tell me about ai",
        "what is java?",
        "explain RAG",
        "what is react paradigm",
        "nonexistent topic"
    ]

    print("\n--- Using retrieve_information (primary for agent) ---")
    for q in queries:
        print(f"Query: \"{q}\" -> Result: \"{retrieve_information(q)}\"")

    print("\n--- Using retrieve_document_simple ---")
    for q in queries:
        print(f"Query: \"{q}\" -> Result: \"{retrieve_document_simple(q)}\"")

    print("\n--- Using retrieve_document_structured ---")
    for q in queries:
        print(f"Query: \"{q}\" -> Result: \"{retrieve_document_structured(q)}\"")

    print(f"Query: \"doc1\" -> Result: \"{retrieve_information('doc1')}\"") # Test ID retrieval
    print(f"Query: \"doc3\" -> Result: \"{retrieve_information('doc3')}\"") # Test ID retrieval
