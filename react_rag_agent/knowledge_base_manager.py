import chromadb
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any

# Define constants
CHROMA_DATA_PATH = "chroma_db_data"  # Folder to store ChromaDB data
COLLECTION_NAME = "rag_documents"
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2" # Efficient and good quality model

# Initialize ChromaDB client (persistent)
try:
    client = chromadb.PersistentClient(path=CHROMA_DATA_PATH)
except Exception as e:
    print(f"Error initializing ChromaDB client: {e}")
    print("Please ensure ChromaDB is installed and configured correctly.")
    # A fallback or further error handling could be implemented here.
    # For this script, we'll let it raise if critical.
    raise

# Initialize sentence transformer model
try:
    embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)
except Exception as e:
    print(f"Error initializing SentenceTransformer model '{EMBEDDING_MODEL_NAME}': {e}")
    print("Please ensure 'sentence-transformers' is installed and the model name is correct.")
    raise

class ChromaEmbeddingFunction(chromadb.EmbeddingFunction):
    """
    Custom embedding function to integrate SentenceTransformer with ChromaDB
    if we want ChromaDB to handle the embedding generation directly during add/query.
    For this manager, we are doing manual embedding before adding.
    However, this class is good for reference or future use.
    """
    def __init__(self, model_name: str = EMBEDDING_MODEL_NAME):
        self.model = SentenceTransformer(model_name)

    def __call__(self, input_texts: chromadb.Documents) -> chromadb.Embeddings:
        return self.model.encode(input_texts).tolist()

def get_or_create_collection(collection_name: str = COLLECTION_NAME) -> chromadb.Collection:
    """
    Gets or creates the ChromaDB collection.
    Uses the custom embedding function if ChromaDB is to generate embeddings.
    For manual embedding, embedding_function can be None or a compatible default.
    To use our specific SentenceTransformer model via Chroma's internal mechanism,
    we would pass an instance of ChromaEmbeddingFunction.
    However, the current add_documents_to_collection shows manual embedding.
    For simplicity with `collection.add`, if embeddings are provided manually,
    the collection can be created without a specific embedding function, or with one
    that matches the dimensionality if not providing embeddings directly (less common for this manual approach).
    Let's ensure it's compatible with manual embedding provision.
    """
    try:
        # If providing embeddings manually with collection.add(),
        # the collection's own embedding function is not strictly used for those adds.
        # However, it's good practice to define it if you might query without providing query_embeddings
        # or add documents without providing embeddings.
        # For now, we'll use a simple default or allow Chroma to handle it.
        # ef = ChromaEmbeddingFunction() # If we wanted Chroma to do the embeddings
        # collection = client.get_or_create_collection(name=collection_name, embedding_function=ef)

        # When adding embeddings manually, embedding_function is not used for that operation.
        # It is used if you `collection.add(documents=["text"])` without `embeddings` param.
        # Or if you `collection.query(query_texts=["text"])` without `query_embeddings` param.
        # Since our `query_collection` also manually embeds, we can be flexible here.
        # Using `sentence_transformers.SentenceTransformer(EMBEDDING_MODEL_NAME).encode("test").shape[0]` for dim
        # For `all-MiniLM-L6-v2`, dimension is 384.
        # ef_metadata = {"hnsw:space": "cosine"} # Optional: configure space
        collection = client.get_or_create_collection(
            name=collection_name,
            # metadata=ef_metadata # Not strictly needed unless customizing index
        )
        print(f"Collection '{collection_name}' retrieved or created successfully.")
        return collection
    except Exception as e:
        print(f"Error getting or creating collection '{collection_name}': {e}")
        raise

def add_documents_to_collection(collection: chromadb.Collection, documents: List[Dict[str, str]], batch_size: int = 100):
    """
    Adds documents to the ChromaDB collection with their embeddings.

    Args:
        collection (chromadb.Collection): The collection to add documents to.
        documents (List[Dict[str, str]]): A list of documents, where each document
                                           is a dictionary with "id" and "text" keys.
        batch_size (int): Number of documents to process and add in a single batch.
    """
    num_documents = len(documents)
    for i in range(0, num_documents, batch_size):
        batch_documents = documents[i:i + batch_size]

        ids = [doc["id"] for doc in batch_documents]
        texts = [doc["text"] for doc in batch_documents]

        print(f"Generating embeddings for batch {i//batch_size + 1} ({len(ids)} documents)...")
        embeddings = embedding_model.encode(texts).tolist()

        try:
            print(f"Adding documents to collection: {ids}")
            # We can also store the original text as metadata if preferred,
            # and use `documents` parameter for something else or not at all if text is in metadata.
            # Here, `documents` parameter in `collection.add` stores the text itself.
            collection.add(
                ids=ids,
                embeddings=embeddings,
                documents=texts, # Storing the text content directly with the vector
                metadatas=[{"source": "local_kb"} for _ in ids] # Example metadata
            )
            print(f"Batch {i//batch_size + 1} added successfully.")
        except Exception as e:
            print(f"Error adding batch {i//batch_size + 1} to collection: {e}")
            # Consider how to handle partial batch failures if necessary
    print(f"All {num_documents} documents processed.")


def query_collection(collection: chromadb.Collection, query_text: str, n_results: int = 1) -> Dict[str, Any]:
    """
    Queries the collection using the given query text.

    Args:
        collection (chromadb.Collection): The collection to query.
        query_text (str): The text to search for.
        n_results (int): The number of results to return.

    Returns:
        Dict[str, Any]: The query results from ChromaDB.
                        Typically includes 'ids', 'documents', 'distances', 'metadatas'.
    """
    print(f"Generating embedding for query: '{query_text}'")
    query_embedding = embedding_model.encode(query_text).tolist()

    try:
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            include=['documents', 'distances', 'metadatas'] # Specify what to include in results
        )
        print(f"Query executed successfully. Found {len(results.get('ids', [[]])[0])} results.")
        return results
    except Exception as e:
        print(f"Error querying collection: {e}")
        raise

# Sample documents from the old knowledge_base.py (can be expanded)
SAMPLE_DOCUMENTS_FOR_DB = [
    {
        "id": "doc1",
        "text": "Python is a versatile, high-level programming language known for its readability and extensive libraries. It was created by Guido van Rossum and first released in 1991."
    },
    {
        "id": "doc2",
        "text": "Java is a class-based, object-oriented programming language designed to have as few implementation dependencies as possible. It is widely used for developing enterprise-level applications."
    },
    {
        "id": "doc3",
        "text": "Artificial intelligence (AI) is intelligence demonstrated by machines, as opposed to the natural intelligence displayed by humans and animals. Key areas include machine learning, natural language processing, and computer vision."
    },
    {
        "id": "doc4",
        "text": "ReAct is a paradigm that combines reasoning and acting in autonomous agents. Agents explicitly generate reasoning traces to make decisions about how to act to complete a task."
    },
    {
        "id": "doc5",
        "text": "Retrieval Augmented Generation (RAG) is a technique where a language model's responses are augmented by retrieving relevant information from an external knowledge base before generating an answer. This helps to make responses more factual and up-to-date."
    }
]

def initialize_and_populate_db():
    """
    Main function to initialize ChromaDB, create a collection, and populate it with sample documents.
    This function is intended to be run once for setup or when document updates are needed.
    """
    print("--- Knowledge Base Manager: Initializing and Populating ChromaDB ---")

    collection = get_or_create_collection()

    # Check if collection is empty or needs repopulation
    # For simplicity, we'll add documents if they don't exist by ID.
    # A more robust check might involve checking all IDs or a version number.
    existing_ids_in_collection = set(collection.get(ids=[doc['id'] for doc in SAMPLE_DOCUMENTS_FOR_DB])['ids'])
    documents_to_add = [doc for doc in SAMPLE_DOCUMENTS_FOR_DB if doc['id'] not in existing_ids_in_collection]

    if documents_to_add:
        print(f"Found {len(documents_to_add)} new documents to add to the collection.")
        add_documents_to_collection(collection, documents_to_add)
    else:
        print("All sample documents already exist in the collection. No new documents added.")

    print(f"\nTotal documents in collection '{COLLECTION_NAME}': {collection.count()}")

    # Perform a sample query
    print("\n--- Performing a sample query ---")
    sample_query = "Tell me about Python programming"
    query_results = query_collection(collection, sample_query, n_results=2)

    print(f"\nResults for query: '{sample_query}'")
    if query_results and query_results.get('documents') and query_results['documents'][0]:
        for i, doc_text in enumerate(query_results['documents'][0]):
            print(f"  Result {i+1}:")
            print(f"    ID: {query_results['ids'][0][i]}")
            print(f"    Distance: {query_results['distances'][0][i]:.4f}")
            print(f"    Text: {doc_text[:100]}...") # Print snippet
            print(f"    Metadata: {query_results['metadatas'][0][i]}")
    else:
        print("  No documents found for the sample query or error in results structure.")

    print("\n--- Knowledge Base Manager: Setup Complete ---")

if __name__ == "__main__":
    initialize_and_populate_db()
