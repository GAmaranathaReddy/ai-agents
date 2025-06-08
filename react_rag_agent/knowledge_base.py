# knowledge_base.py

DOCUMENTS = {
    "python": "Python is a versatile, high-level programming language known for its readability and extensive libraries. It was created by Guido van Rossum and first released in 1991.",
    "java": "Java is a class-based, object-oriented programming language designed to have as few implementation dependencies as possible. It is widely used for developing enterprise-level applications.",
    "ai": "Artificial intelligence (AI) is intelligence demonstrated by machines, as opposed to the natural intelligence displayed by humans and animals. Key areas include machine learning, natural language processing, and computer vision.",
    "react": "ReAct is a paradigm that combines reasoning and acting in autonomous agents. Agents explicitly generate reasoning traces to make decisions about how to act to complete a task.",
    "rag": "Retrieval Augmented Generation (RAG) is a technique where a language model's responses are augmented by retrieving relevant information from an external knowledge base before generating an answer. This helps to make responses more factual and up-to-date."
}

# Example of a more structured knowledge base if needed later
STRUCTURED_DOCUMENTS = [
    {
        "id": "doc1",
        "keywords": ["python", "programming language", "guido van rossum"],
        "text": "Python is a versatile, high-level programming language known for its readability and extensive libraries. It was created by Guido van Rossum and first released in 1991.",
        "category": "programming"
    },
    {
        "id": "doc2",
        "keywords": ["java", "object-oriented", "enterprise applications"],
        "text": "Java is a class-based, object-oriented programming language designed to have as few implementation dependencies as possible. It is widely used for developing enterprise-level applications.",
        "category": "programming"
    },
    {
        "id": "doc3",
        "keywords": ["ai", "artificial intelligence", "machine learning", "nlp"],
        "text": "Artificial intelligence (AI) is intelligence demonstrated by machines, as opposed to the natural intelligence displayed by humans and animals. Key areas include machine learning, natural language processing, and computer vision.",
        "category": "technology"
    },
    {
        "id": "doc4",
        "keywords": ["react", "reasoning", "acting", "autonomous agents"],
        "text": "ReAct is a paradigm that combines reasoning and acting in autonomous agents. Agents explicitly generate reasoning traces to make decisions about how to act to complete a task.",
        "category": "ai concepts"
    },
    {
        "id": "doc5",
        "keywords": ["rag", "retrieval augmented generation", "language model"],
        "text": "Retrieval Augmented Generation (RAG) is a technique where a language model's responses are augmented by retrieving relevant information from an external knowledge base before generating an answer. This helps to make responses more factual and up-to-date.",
        "category": "ai concepts"
    }
]

def get_document_by_id(doc_id: str) -> dict | None:
    """
    Retrieves a document by its ID from the structured knowledge base.
    """
    for doc in STRUCTURED_DOCUMENTS:
        if doc["id"] == doc_id:
            return doc
    return None

if __name__ == '__main__':
    print("Available simple documents (keys):", list(DOCUMENTS.keys()))
    print("\nAvailable structured documents (IDs):", [d['id'] for d in STRUCTURED_DOCUMENTS])

    print("\nTesting get_document_by_id('doc1'):")
    print(get_document_by_id('doc1'))

    print("\nTesting get_document_by_id('doc_unknown'):")
    print(get_document_by_id('doc_unknown'))
