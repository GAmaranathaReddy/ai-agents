![Python 3.12](https://img.shields.io/badge/python-3.12-blue)  ![phidata](https://img.shields.io/badge/phidata-orange) ![ollama](https://img.shields.io/badge/ollama-white) 

# Example App

[About](#about) • [Agents](#agents) • [Getting Started](#getting-started) • [Additional Notes](#additional-notes) • [Contributors](#contributors)

## About

AI agents automate tasks, enhance decision-making, improve personalization, provide 24/7 availability, scale efficiently, reduce costs, increase accuracy, solve complex problems, enable accessibility, and drive innovation.

I am creating a tutorial on agents, covering various types. The tutorial includes Python Poetry projects designed to run locally using Ollama models and a local database, ensuring data privacy. This approach eliminates the need to spend money on purchasing API keys 


![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/colored.png)

## Multi-LLM Provider Support

This project now supports multiple Large Language Model (LLM) providers, allowing you to choose the backend that best suits your needs. The supported providers are:

- **Ollama**: For running models locally (default).
- **OpenAI**: Access to models like GPT-3.5, GPT-4.
- **Google Gemini**: Access to Gemini models.
- **AWS Bedrock**: Access to various models hosted on AWS Bedrock (e.g., Anthropic Claude, Meta Llama, Amazon Titan).

### Configuration via Environment Variables

You can configure the desired provider and associated settings using environment variables:

- `LLM_PROVIDER`: Specifies the provider to use.
  - Values: `"ollama"`, `"openai"`, `"gemini"`, `"bedrock"`
  - Default: `"ollama"`
- `OLLAMA_MODEL`: Model name for Ollama (e.g., `"mistral"`, `"llama2"`). Default: `"mistral"`.
- `OLLAMA_HOST`: (Optional) URL for the Ollama service if not default `http://localhost:11434`.
- `OPENAI_MODEL`: Model name for OpenAI (e.g., `"gpt-3.5-turbo"`, `"gpt-4"`). Default: `"gpt-3.5-turbo"`.
- `OPENAI_API_KEY`: Your OpenAI API key.
- `GEMINI_MODEL`: Model name for Google Gemini (e.g., `"gemini-pro"`). Default: `"gemini-pro"`.
- `GOOGLE_API_KEY`: Your Google API key (often for Gemini via AI Studio).
- `BEDROCK_MODEL`: Model ID for AWS Bedrock (e.g., `"anthropic.claude-3-sonnet-20240229-v1:0"`). Default: `"anthropic.claude-3-sonnet-20240229-v1:0"`.
- `AWS_BEDROCK_REGION`: The AWS region where you are using Bedrock (e.g., `"us-east-1"`). Can also use `AWS_REGION` or `AWS_DEFAULT_REGION`.
- `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_SESSION_TOKEN`: Your AWS credentials (if not using IAM roles or other default AWS credential mechanisms).

The agents will automatically use the configured provider. Make sure you have installed the necessary Python SDK for your chosen provider (see "Dependencies" below).

### Provider-Specific SDK Dependencies

Depending on the `LLM_PROVIDER` you choose, you may need to install additional Python libraries. The core agents will list these in their individual `README.md` files, but the common ones are:

- **Ollama**: `pip install ollama`
- **OpenAI**: `pip install openai`
- **Google Gemini**: `pip install google-generativeai`
- **AWS Bedrock**: `pip install boto3`

These should also be added to a root `requirements.txt` if you plan to use multiple providers.

Refer to the [Common Utilities README](./common/README.md) for more details on the LLM configuration and provider abstraction layer.

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/colored.png)

## Agents

  - [Web Search](https://github.com/GAmaranathaReddy/ai-agents/tree/main/web-rearch-agent)
    - [Code WalkThough](https://youtu.be/j6x0PKXi1RA)
  - [Data Analyst](https://github.com/GAmaranathaReddy/ai-agents/tree/main/data_analyst)
  - [Fianace Agent](https://github.com/GAmaranathaReddy/ai-agents/tree/main/finance_agent)
    - [Code WalkThough](https://youtu.be/XPWWGjytBKU)
  - [Health Fitness Agent](https://github.com/GAmaranathaReddy/ai-agents/tree/main/ai_health_fitness_agent)
  - **Agentic Design Patterns**
    - [LLM-Enhanced Agent](./llm_enhanced_agent/): Demonstrates enhancing an agent's capabilities with (simulated) LLM interaction.
      - *Use Case:* A customer service bot that uses an LLM to understand user queries and generate natural-sounding responses.
    - [Fixed Automation Agent](./fixed_automation_agent/): Shows a rule-based agent performing predefined tasks.
      - *Use Case:* An automated system for daily report generation where the steps are fixed and predictable.
    - [ReAct + RAG Agent](./react_rag_agent/): Implements a simplified Reason-Act loop with Retrieval Augmented Generation.
      - *Use Case:* A research assistant that can break down a complex question, search a knowledge base for relevant information, and synthesize an answer.
    - [Tool-Enhanced Agent](./tool_enhanced_agent/): An agent that can select and use various tools based on user input.
      - *Use Case:* A personal assistant that books appointments (calendar API), checks weather (weather API), and manages to-do lists.
    - [Self-Reflecting Agent](./self_reflecting_agent/): An agent that performs a task, critiques its own output, and attempts to refine it.
      - *Use Case:* An AI writing assistant that generates a draft, reviews it for tone/clarity/grammar, and refines it.
    - [Memory-Enhanced Agent](./memory_enhanced_agent/): An agent that stores and recalls information from past interactions.
      - *Use Case:* A personalized learning tutor that remembers a student's past performance to tailor future lessons.
    - [Environment-Controlled Agent](./environment_controlled_agent/): An agent that perceives and acts within a simple simulated environment.
      - *Use Case:* A robotic vacuum cleaner that navigates a room, detects obstacles, and adjusts its path based on sensor inputs.
    - [Self-Learning Agent](./self_learning_agent/): A Rock-Paper-Scissors agent that adapts its strategy based on opponent's moves.
      - *Use Case:* A game AI that improves its playing strategy over time by learning from wins/losses against opponents.

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/colored.png)

## Getting Started

### Pre-requisites

- [Python 3.12](https://www.python.org/downloads)
- [Poetry](https://python-poetry.org/docs/#installation)
- [ollama](https://ollama.com/download)

### Setting Up Development Environment in Local


Clone the project

```bash
  git clone https://github.com/GAmaranathaReddy/ai-agents.git
```

Go to the agent directory

```bash
  cd <<agent directory>>
```

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/colored.png)

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



![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/colored.png)


## Additional Notes

To be added

## Contributors

To be added
