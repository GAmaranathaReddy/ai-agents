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

This project demonstrates an advanced ReAct + RAG flow. The agent's **Reasoning** (intent analysis, search query formulation) and final **Response Synthesis** are powered by a dynamically selectable LLM provider accessed via the **common LLM abstraction layer** (`common.llm_providers.client`). The **Retrieval** part uses ChromaDB.

1.  **`common/llm_providers/` (Abstraction Layer)**:
    *   Provides `get_llm_client` to instantiate providers like Ollama, OpenAI, Gemini, Bedrock.

2.  **`react_rag_agent/knowledge_base_manager.py`**:
    *   Manages the ChromaDB vector store using `sentence-transformers` for embeddings.
    *   Run `python react_rag_agent/knowledge_base_manager.py` once to initialize/populate the DB with sample documents. Data is stored in `./react_rag_agent/chroma_db_data/`.

3.  **`react_rag_agent/tools.py`**:
    *   The `retrieve_information(query)` function interfaces with `knowledge_base_manager.py` to fetch relevant documents from ChromaDB.

4.  **`react_rag_agent/agent.py` (`ReActRAGAgent` class - Refactored)**:
    *   **LLM Abstraction**: No longer directly imports specific LLM SDKs (like `ollama`). It imports `get_llm_client` from the common abstraction layer.
    *   **Initialization**: `__init__(provider_name, model_name, **provider_kwargs)` allows specifying the LLM provider and model. It initializes `self.llm_client` using the factory. It determines `self.llm_model` to use (e.g., "mistral", "gpt-3.5-turbo-1106", "anthropic.claude-3-sonnet-20240229-v1:0") based on the input, provider defaults, or agent-specific defaults suitable for reasoning and JSON output.
    *   **`reason_and_act(user_input: str)` Method - Core Logic**:
        1.  **Phase 1: Query Analysis & Search Query Formulation (LLM Call 1 via Abstraction)**:
            *   The agent sends the `user_input` to `self.llm_client.chat(model=self.llm_model, ..., format_json=True)`.
            *   The prompt guides the LLM to determine intent, generate a `search_query` (if "information_seeking"), or provide a direct `llm_response`, all in JSON format.
        2.  **Phase 2: Retrieval (Action)**:
            *   If "information_seeking", the LLM-generated `search_query` is used with `retrieve_information()` to query ChromaDB.
        3.  **Phase 3: Response Synthesis (LLM Call 2 via Abstraction or Direct Answer)**:
            *   If context was retrieved, a second call to `self.llm_client.chat(model=self.llm_model, ..., format_json=False)` synthesizes the final answer.
            *   If a direct answer was available from Phase 1, it's used. Fallbacks are in place.
        4.  **Output**: Returns a structured dictionary ( `thought_process`, `action_taken`, etc.).

5.  **`react_rag_agent/app_ui.py` (Streamlit UI - Enhanced)**:
    *   Allows dynamic selection of the LLM provider (Ollama, OpenAI, Gemini, Bedrock) and model name via sidebar widgets.
    *   Re-initializes the `ReActRAGAgent` with the new selections.
    *   Displays current provider/model and notes about API keys.

6.  **`knowledge_base.py` (DELETED)**: The old dictionary-based KB is removed.

The agent's flow:
User Input -> **LLM (Analysis via Abstraction Layer)** -> [Optional: Tool (ChromaDB Retrieval)] -> **LLM (Synthesis via Abstraction Layer)** -> Final Response.

## Prerequisites & Setup

1.  **Install Python Dependencies**:
    Install all packages from `react_rag_agent/requirements.txt`. This includes `streamlit`, `chromadb`, `sentence-transformers`, and LLM SDKs (`ollama`, `openai`, `google-generativeai`, `boto3`).
    ```bash
    pip install -r react_rag_agent/requirements.txt
    ```

2.  **Knowledge Base (ChromaDB)**:
    *   Initialize and populate the database by running *once*:
      ```bash
      python react_rag_agent/knowledge_base_manager.py
      ```

3.  **LLM Provider Setup (Choose one or more as needed)**:
    *   **Ollama**: Install from [ollama.com](https://ollama.com/), ensure service is running, and pull a model (e.g., `ollama pull mistral`).
    *   **OpenAI**: Set `OPENAI_API_KEY` environment variable.
    *   **Google Gemini**: Set `GOOGLE_API_KEY` environment variable.
    *   **AWS Bedrock**: Configure AWS credentials and region. Ensure model access.
    *(Refer to the main project README for more detailed setup instructions for each provider if needed.)*

## How to Run

**(Ensure all Prerequisites & Setup are complete: Python packages installed, ChromaDB initialized, and chosen LLM provider(s) configured.)**

1.  **Navigate to the repository root** (for Streamlit UI) or **agent's directory** (for CLI):
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
