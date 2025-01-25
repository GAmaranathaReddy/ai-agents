# Web Search Agent

The Web Search Agent is an AI-powered chatbot that allows users to search the web and get answers with included sources. Built using Streamlit, this chatbot uses the Ollama LLM and DuckDuckGo search tool to provide accurate and comprehensive responses.

---

## Features

- **Web Search Capabilities**: Uses DuckDuckGo to fetch relevant information from the web.
- **Interactive Chat Interface**: Chat-like UI for seamless interaction.
- **Source Inclusion**: Ensures that all responses include sources for transparency.
- **Streamlit Framework**: Lightweight and easy-to-deploy application.

---

## Installation

### Prerequisites
Ensure you have the following installed on your system:

1. Python 3.12 or higher
2. Streamlit
3. Required Python libraries:
   - `streamlit`
   - `streamlit_chat`
   - `phi`
  
## How Works

<img width="803" alt="image" src="https://github.com/user-attachments/assets/10de28c6-2cce-4bff-a95e-9ea8d96db4aa" />

### Setting Up Development Environment in Local

Clone the project
```bash
  git clone https://github.com/GAmaranathaReddy/ai-agents.git
```
Go to the agent directory
```bash
  cd ai_health_fitness_agent
```
### Run using Poetry

#### Set up development environment
```bash
  poetry env use python3.12
```
This configures Poetry to use Python 3.12 as the interpreter for the project's virtual environment.

#### Install dependencies
```bash
  poetry install
```

This installs all dependencies specified in the pyproject.toml on each agent project file

3. Run the application:
   ```bash
   streamlit run run.py
   ```

---

## Usage

1. Open the application in your browser (Streamlit will provide a local URL).
2. Enter your query in the chat input box.
3. Press the **Send** button to submit your query.
4. The chatbot will display the response with included sources.

---

## Dependencies

- `streamlit`
- `streamlit_chat`
- `phi`
- `ollama`
- `duckduckgo`

---

## Contributing

1. Fork the repository.
2. Create a feature branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add new feature"
   ```
4. Push the branch:
   ```bash
   git push origin feature-name
   ```
5. Open a pull request.

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

## Acknowledgments

- **Streamlit**: For providing an easy-to-use framework for building web applications.
- **Ollama**: For powering the chatbot with advanced language model capabilities.
- **DuckDuckGo**: For enabling secure and efficient web searches.

