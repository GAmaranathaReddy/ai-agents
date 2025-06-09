# ReAct + RAG Agent

## ReAct and RAG Patterns

**ReAct (Reason and Act)**:
ReAct is an agent paradigm that emphasizes the synergy between *reasoning* and *acting*. Instead of just taking an input and producing an output, a ReAct agent goes through an explicit thought process. It might:
1.  **Observe**: Take in the user query and current state.
2.  **Think/Reason**: Decide what to do next. This could involve breaking down the problem, identifying if external tools are needed, or formulating a sub-query. The reasoning steps are often explicit and can be logged (like a "chain of thought").
3.  **Act**: Execute the chosen action. This might be calling a tool (like a search engine, a calculator, or a knowledge base retriever), asking a clarifying question, or generating a partial response.
4.  **Observe**: Evaluate the result of the action.
This loop continues until the agent can produce a final answer. The key is making the reasoning process overt, which allows for more complex task handling and better debugging.

**RAG (Retrieval Augmented Generation)**:
RAG is a technique specifically for language models (LMs) or generative agents. It aims to improve the quality, accuracy, and relevance of generated responses by:
1.  **Retrieving**: Before generating a response, the system retrieves relevant information from an external knowledge source (e.g., a vector database, a document store, a set of APIs). The user's query is often used to find these relevant pieces of information.
2.  **Augmenting**: The retrieved information is then provided as context to the language model along with the original query.
3.  **Generating**: The language model uses both the original query and the augmented context to generate its final response.
RAG helps to ground the LM's responses in factual data, reduce hallucinations, and allow the model to use information it wasn't originally trained on.

**ReAct + RAG**:
Combining ReAct and RAG creates a powerful agent. The ReAct framework provides the overall decision-making loop (reason about what's needed, act to get it). RAG is often one of the "actions" the ReAct agent can take: if the agent reasons that it needs external knowledge to answer a query, it "acts" by performing a retrieval (the RAG part), and then uses the retrieved information to generate the final response.

## Implementation

This project demonstrates an advanced ReAct + RAG flow where the **Reasoning** and **Generation** aspects are powered by a Large Language Model (LLM) via Ollama, and the **Retrieval** part uses ChromaDB as a vector store.

1.  **`knowledge_base_manager.py`**:
    *   Manages the ChromaDB vector database.
    *   Uses `sentence-transformers` (e.g., `all-MiniLM-L6-v2`) for embedding documents and queries.
    *   Handles ChromaDB client initialization, collection management, document addition (with embeddings), and querying.
    *   Running `python react_rag_agent/knowledge_base_manager.py` initializes and populates the DB.

2.  **`tools.py`**:
    *   The `retrieve_information(query)` function interfaces with `knowledge_base_manager.py` to fetch relevant documents from ChromaDB based on semantic similarity.

3.  **`agent.py` (`ReActRAGAgent` class - Significantly Updated)**:
    *   **LLM Integration**: Imports `ollama` and `json`. It's initialized with an Ollama model name (e.g., "mistral") for its reasoning and generation tasks.
    *   **`reason_and_act(user_input: str)` Method - Core Logic**:
        1.  **Phase 1: Query Analysis & Search Query Formulation (LLM Call 1)**:
            *   The agent first sends the `user_input` to the LLM (e.g., Mistral via Ollama).
            *   A carefully crafted prompt instructs the LLM to:
                *   Determine the user's `intent`: Is it "information_seeking" (requiring KB lookup) or "direct_answer" (general chat/question)?
                *   If "information_seeking", generate a concise `search_query` suitable for the vector database.
                *   If "direct_answer", generate a preliminary `llm_response`.
            *   The LLM is asked to return this analysis in **JSON format**. The agent parses this JSON.
            *   Includes error handling for the LLM call and JSON parsing, with fallbacks (e.g., defaulting to using the original user input as the search query).
            *   The agent logs these initial reasoning steps.
        2.  **Phase 2: Retrieval (Action, if "information_seeking")**:
            *   If the LLM identified the intent as "information_seeking" and provided a `search_query`:
                *   The agent calls `retrieve_information(search_query)` (from `tools.py`), which queries ChromaDB.
                *   The retrieved document(s) are stored.
            *   The agent logs the retrieval action and its outcome.
        3.  **Phase 3: Response Synthesis (LLM Call 2 or Direct Answer)**:
            *   **If information was retrieved**: The agent makes a *second* call to the LLM. This prompt includes the original `user_input` and the `retrieved_info` from ChromaDB. The LLM is asked to synthesize a comprehensive final answer based on both.
            *   **If no retrieval was needed (intent was "direct_answer")**: The `llm_response` from Phase 1 is used as the final answer.
            *   **Fallback**: If errors occurred or no useful information was obtained, a default or LLM-generated general response is provided.
        4.  **Output**: The method returns a dictionary containing a detailed `thought_process` (list of steps), `action_taken` (describing the multi-step process), the `query_for_retrieval` (if any), `retrieved_info` (if any), and the `final_response`.

4.  **`main.py` (CLI)** and **`app_ui.py` (Streamlit UI)**:
    *   These interfaces interact with the agent. The Streamlit UI is particularly helpful for visualizing the detailed `thought_process`, `action_taken`, `retrieved_info`, and `final_response` from the agent's structured output.

5.  **`knowledge_base.py` (DELETED)**:
    *   The old dictionary-based KB is obsolete and has been removed.

The agent's flow is now more sophisticated:
User Input -> **LLM (Analysis: Intent & Search Query Generation)** -> [Optional: Tool (ChromaDB Retrieval using generated query)] -> **LLM (Synthesis using retrieved context if available, or direct answer)** -> Final Response.

## Prerequisites & Setup

### 1. Ollama and LLM Model
   *   **Install Ollama**: Ensure Ollama is installed and running. See the [Ollama official website](https://ollama.com/).
   *   **Pull an LLM Model**: The agent defaults to `"mistral"`. You need this model (or your chosen alternative) pulled in Ollama.
     ```bash
     ollama pull mistral
     ```
     For potentially better JSON handling and instruction following required by this agent, models like `"mistral"` or `"nous-hermes2"` (or other fine-tuned instruction models) are recommended. Ensure the model specified in `agent.py` is available.
   *   **Install Ollama Python Client**:
     ```bash
     pip install ollama
     ```

### 2. Knowledge Base (ChromaDB)
    *   **Install Dependencies**: You'll need `chromadb` and `sentence-transformers`.
      ```bash
      pip install chromadb sentence-transformers
      ```
    *   **Initialize and Populate Database**: Run the knowledge base manager script *once* before using the agent:
      ```bash
      python react_rag_agent/knowledge_base_manager.py
      ```
      This creates a local ChromaDB instance in `./react_rag_agent/chroma_db_data/` and populates it with sample documents.

*(If using Poetry for the main project, add `ollama`, `chromadb`, and `sentence-transformers` to your `pyproject.toml` and run `poetry install`.)*

## How to Run

**(Ensure you have completed all Prerequisites & Setup steps above: Ollama running, model pulled, Python packages installed, and ChromaDB initialized.)**

1.  **Navigate to the agent's directory** (if running CLI) or **repository root** (if running Streamlit UI):
    Before running the agent (CLI or UI) for the first time, or whenever you want to ensure the KB is set up with the sample documents, run the `knowledge_base_manager.py` script once:
    ```bash
    python react_rag_agent/knowledge_base_manager.py
    ```
    This script will:
    *   Create a persistent ChromaDB database in a folder named `chroma_db_data` within the `react_rag_agent` directory.
    *   Define a collection named `rag_documents`.
    *   Add a set of sample documents (related to Python, Java, AI, ReAct, RAG) to the collection, generating their embeddings using the `all-MiniLM-L6-v2` model.
    *   Perform a test query to confirm setup.
    You only need to run this script once initially, or if you modify the sample documents within `knowledge_base_manager.py` and want to re-populate the database.

## How to Run

**(Ensure you have completed the Knowledge Base Setup above first.)**

1.  **Navigate to the agent's directory** (if running CLI) or **repository root** (if running Streamlit UI):
    For CLI:
    ```bash
    cd path/to/your/react_rag_agent
    ```
    For Streamlit UI (assuming it's run from root):
    ```bash
    cd path/to/your/repository_root
    ```

2.  **Run the `main.py` script (CLI)**:
    (Ensure you are in the `react_rag_agent` directory)
    ```bash
    python main.py
    ```
    Or, if you have multiple Python versions:
    ```bash
    python3 main.py
    ```
    *(The CLI and UI now use the ChromaDB-backed knowledge base.)*

3.  **Interact with the Agent via CLI**:
    The CLI will start. Try asking questions about the topics in the knowledge base.
    ```
    ReAct-RAG Agent CLI
    Ask about topics like Python, Java, AI, ReAct, or RAG.
    Try phrases like 'tell me about python', 'what is ai?', 'explain rag'.
    ------------------------------
    You: tell me about python
    Agent: Based on available information about 'python': Python is a versatile, high-level programming language known for its readability and extensive libraries. It was created by Guido van Rossum and first released in 1991.
    You: what is RAG?
    Agent: Based on available information about 'rag': Retrieval Augmented Generation (RAG) is a technique where a language model's responses are augmented by retrieving relevant information from an external knowledge base before generating an answer. This helps to make responses more factual and up-to-date.
    You: doc1
    Agent: Based on available information about 'doc1': Python is a versatile, high-level programming language known for its readability and extensive libraries. It was created by Guido van Rossum and first released in 1991.
    You: What is the capital of France?
    Agent: I tried to find information about 'the capital of france?', but I couldn't find anything specific in my knowledge base.
    You: exit
    Exiting agent CLI. Goodbye!
    ```

### Web UI (Streamlit)

This ReAct + RAG agent also has a web-based user interface built with Streamlit, allowing for a more visual interaction with its reasoning process.

1.  **Install Streamlit**:
    If you haven't done so already, install Streamlit. If your main project uses Poetry, consider adding Streamlit as a dependency there. For a standard local installation:
    ```bash
    pip install streamlit
    ```

2.  **Run the Streamlit App**:
    To start the web UI, open your terminal, navigate to the root directory of this repository (where the main `README.md` is), and execute the command:
    ```bash
    streamlit run react_rag_agent/app_ui.py
    ```
    This will typically launch the application in your default web browser.

3.  **Interact with the Agent via Web**:
    *   The web interface will present a title, a brief explanation, and a text input field for your query.
    *   A sidebar will show some of the keywords the agent knows about from its knowledge base.
    *   Enter your query (e.g., "tell me about AI", "what is react?", "doc3").
    *   Click the "Submit to Agent" button.
    *   The UI will then display:
        *   An expandable section showing the agent's internal "Thought Process".
        *   Details about any "Action Taken" (like retrieval), the query used, and a snippet of the "Retrieved Information".
        *   The "Final Response" from the agent.
    This allows you to see how the agent arrived at its answer.
