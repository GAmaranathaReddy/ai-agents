# Finance Agent Application

## Overview
The **Finance Agent Application** is a multi-functional agent platform designed to assist with finance-related queries and general web searches. This application leverages advanced LLM models, financial tools, and web search capabilities to provide data-driven responses and actionable insights.

### Key Features
- **Finance Agent**:
  - Retrieves real-time stock prices, analyst recommendations, company information, and news.
  - Presents financial data in table format for better readability.
- **Web Agent**:
  - Conducts general web searches using DuckDuckGo.
  - Always includes sources in the responses.
- **Data Persistence**:
  - Stores agent interactions and history in an SQLite database for future reference.
- **User-Friendly Interface**:
  - Includes a playground app for interacting with agents in an intuitive way.

---

## How to Run the Application

### Prerequisites
- **Python 3.12 or higher**
- Required Python packages:
  - `phi`
  - `duckduckgo-search`
  - `yfinance`
  - Any other dependencies listed in `pyproject.toml`

### Installation Steps
### Setting Up Development Environment in Local

Clone the project

```bash
  git clone https://github.com/GAmaranathaReddy/ai-agents.git
```

Go to the agent directory

```bash
  cd finance_agent
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

## Agents Description

### 1. **Finance Agent**
- **Purpose**: Provides comprehensive financial information and analysis.
- **Capabilities**:
  - Fetches real-time stock prices.
  - Delivers analyst recommendations.
  - Retrieves company profiles and news updates.
- **Tools**: Utilizes `YFinanceTools` for financial data.
- **Storage**: Interaction history is stored in `agents.db` under the `finance_agent` table.

### 2. **Web Agent**
- **Purpose**: Performs general-purpose web searches.
- **Capabilities**:
  - Executes searches via DuckDuckGo.
  - Includes reliable sources in the response.
- **Tools**: Leverages `DuckDuckGo` for web searches.
- **Storage**: Interaction history is stored in `agents.db` under the `web_agent` table.

---

## Application Structure
- **Agents**:
  - Defined using the `Agent` class from the `phi` library.
  - Configured with specific tools and instructions.
- **Playground App**:
  - Built using `phi.playground` for an interactive agent experience.
  - Configured to serve both the Finance and Web agents.
- **Storage**:
  - SQLite database (`agents.db`) used to persist agent interactions.
- **Main Entry Point**:
  - `serve_playground_app` starts the application and reloads on code changes.

---

## Customization
1. **Modify Agent Configuration**:
   - Update agent names, tools, or instructions as needed.
2. **Extend Tools**:
   - Add or customize tools for specific use cases.
3. **Update Storage Settings**:
   - Change the database file or table names to suit your requirements.

---

## Troubleshooting

### Common Issues
1. **Dependencies Missing**:
   - Ensure all dependencies are installed using `poetry install`.
2. **Port Already in Use**:
   - Modify the default port in `serve_playground_app` if it conflicts with another application.
3. **Data Not Persisting**:
   - Check that the `agents.db` file exists and has the correct permissions.

### Logs
- Check the terminal output for real-time logs and error messages.

---

## License
This project is licensed under the [MIT License](LICENSE).

---

## Acknowledgments
- **Phi Library**: For enabling agent and tool integration.
- **DuckDuckGo**: For web search capabilities.
- **Yahoo Finance**: For financial data retrieval.

---

## Feedback and Contributions
Feel free to open issues or submit pull requests for bug fixes, feature requests, or improvements. Contributions are welcome!

