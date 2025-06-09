# tools.py
# Now uses ChromaDB for retrieval via knowledge_base_manager
from react_rag_agent.knowledge_base_manager import get_or_create_collection, query_collection, COLLECTION_NAME

# The old functions retrieve_document_simple and retrieve_document_structured are removed
# as their functionality is replaced by querying ChromaDB.

def retrieve_information(query: str, n_results: int = 1) -> str:
    """
    Primary retrieval function for the agent.
    Queries the ChromaDB collection for relevant documents.

    Args:
        query (str): The user's query text.
        n_results (int): Number of results to retrieve from ChromaDB.

    Returns:
        str: A formatted string containing the retrieved document(s) or a "not found" message.
    """
    try:
        collection = get_or_create_collection(collection_name=COLLECTION_NAME)
        query_results = query_collection(collection, query_text=query, n_results=n_results)

        if query_results and query_results.get('documents') and query_results['documents'][0]:
            # Assuming documents[0] is a list of document texts for the first query
            # For n_results=1, this will be a list with one document.
            # We can concatenate if n_results > 1, or just return the top one.

            # Example: Return the text of the top document
            # top_document_text = query_results['documents'][0][0]
            # top_document_id = query_results['ids'][0][0]
            # top_document_distance = query_results['distances'][0][0]
            # top_document_metadata = query_results['metadatas'][0][0]
            # return f"Retrieved (ID: {top_document_id}, Distance: {top_document_distance:.4f}): \"{top_document_text}\" (Source: {top_document_metadata.get('source', 'N/A')})"

            # Concatenate multiple results if n_results > 1
            formatted_results = []
            for i in range(len(query_results['documents'][0])):
                doc_text = query_results['documents'][0][i]
                doc_id = query_results['ids'][0][i]
                doc_distance = query_results['distances'][0][i]
                doc_metadata = query_results['metadatas'][0][i]
                formatted_results.append(
                    f"Doc ID {doc_id} (Similarity: {1-doc_distance:.2f}): {doc_text}"
                    # Chroma often returns cosine distance (0=identical, 1=different), so 1-dist can be similarity.
                    # Or simply show distance: (Distance: {doc_distance:.4f})
                )
            return "\n".join(formatted_results)

        else:
            return "No relevant document found in ChromaDB for your query."
    except Exception as e:
        print(f"Error during retrieve_information: {e}")
        return f"Error retrieving information from ChromaDB: {e}"

if __name__ == '__main__':
    print("Testing tools.py with ChromaDB integration...")
    print("Ensure ChromaDB is populated by running knowledge_base_manager.py first.")

    test_queries = [
        "What is Python?",
        "Tell me about AI",
        "Explain RAG technology",
        "What is ReAct?",
        "Information on Java language",
        "A topic not in the database like 'underwater basket weaving'"
    ]

    print("\n--- Testing retrieve_information (from ChromaDB) ---")
    for q_text in test_queries:
        print(f"\nQuery: \"{q_text}\"")
        retrieved_docs = retrieve_information(q_text, n_results=2) # Ask for 2 results
        print(f"Result:\n{retrieved_docs}")

    # Test with a query that might match a specific ID if IDs are descriptive or part of text
    # (Though ChromaDB primarily matches on semantic content of the text)
    print(f"\nQuery: \"doc1\"") # This will search for the text "doc1" semantically
    retrieved_docs_id_query = retrieve_information("doc1", n_results=1)
    print(f"Result:\n{retrieved_docs_id_query}")

    print(f"\nQuery: \"Python programming language\"") # More specific query
    retrieved_docs_specific = retrieve_information("Python programming language", n_results=1)
    print(f"Result:\n{retrieved_docs_specific}")
