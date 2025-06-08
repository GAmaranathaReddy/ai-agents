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

This project demonstrates a simplified ReAct + RAG flow:

1.  **`knowledge_base.py`**:
    *   Defines two simple Python dictionaries (`DOCUMENTS` and `STRUCTURED_DOCUMENTS`) that act as our external knowledge store. This is the "KB" that RAG will retrieve from.

2.  **`tools.py`**:
    *   Defines `retrieve_information(query)` function. This function simulates a retrieval tool.
    *   It searches the `DOCUMENTS` and `STRUCTURED_DOCUMENTS` in `knowledge_base.py` for text relevant to the `query`.
    *   This is the "Retrieval" part of RAG, and it's an "Action" the ReAct agent can perform.

3.  **`agent.py`**:
    *   Defines the `ReActRAGAgent` class.
    *   The `reason_and_act(user_input)` method is the core:
        *   **Reasoning**: It analyzes the `user_input`.
            *   It checks if the input matches specific keywords (e.g., "python", "ai", "doc1") or phrases (e.g., "tell me about", "what is").
            *   Based on this analysis, it decides whether it needs to use the `retrieve_information` tool. This decision is logged in a `thought_process` list (simulating the explicit reasoning of ReAct).
        *   **Acting**: If the reasoning step determines a retrieval is necessary, it calls `retrieve_information(query_for_retrieval)` with the appropriate query. The result (or lack thereof) is an "Observation."
        *   **Generation**: It then formulates a response.
            *   If information was successfully retrieved, the response is *augmented* with this information (this is the "Augmented Generation" part of RAG).
            *   If no retrieval was deemed necessary, or if retrieval failed, it provides a default or alternative response.
    *   The agent's internal `thought_process` (though not fully exposed in the final CLI output for brevity) shows the ReAct cycle: analyzing input, deciding on an action (retrieval), executing the action, and observing the outcome to generate a final response.

4.  **`main.py`**:
    *   Provides a simple command-line interface (CLI) to interact with the `ReActRAGAgent`.

The flow is:
User Input -> Agent Reasons (is retrieval needed?) -> Agent Acts (calls `retrieve_information`) -> Agent Gets Observation (retrieved text) -> Agent Generates Response (using retrieved text).

## How to Run

1.  **Navigate to the project directory**:
    Open your terminal or command prompt.
    ```bash
    cd path/to/your/react_rag_agent
    ```

2.  **Ensure all files are present**:
    You should have `agent.py`, `tools.py`, `knowledge_base.py`, and `main.py` in this directory.

3.  **Run the `main.py` script**:
    ```bash
    python main.py
    ```
    Or, if you have multiple Python versions, you might need to use `python3`:
    ```bash
    python3 main.py
    ```

4.  **Interact with the Agent**:
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
