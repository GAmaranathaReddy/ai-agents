# Data Analyst Agent

This project is a Streamlit application designed to act as a **Data Analyst Agent**. It allows users to upload CSV or Excel files, preprocess the data, and generate insights or queries using a DuckDbAgent backed by a semantic model. Users can interact with the agent by asking questions about their uploaded data.

## Features

- **File Upload**: Supports CSV and Excel files.
- **Data Preprocessing**:
  - Converts date and numeric columns automatically.
  - Handles missing values (`NA`, `N/A`, `missing`).
  - Ensures proper quoting of string fields.
- **Interactive Table Display**: Displays uploaded data in an interactive format.
- **SQL Query Generation**: Leverages DuckDbAgent to generate SQL queries and provide responses to user queries about the data.
- **Semantic Model Integration**: Configures semantic models dynamically for uploaded data.

## Requirements

- **Python**: Ensure Python is installed on your system.
- **Libraries**:
  - `streamlit`
  - `pandas`
  - `phi`

## Installation

### Setting Up Development Environment in Local


Clone the project

```bash
  git clone https://github.com/GAmaranathaReddy/ai-agents.git
```

Go to the agent directory

```bash
  cd data_analyst
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

## Usage

1. **Launch the App**:
   Run the Streamlit application using the command above.


3. **Upload a File**:
   - Click the "Upload a CSV or Excel file" button.
   - Ensure the file is in CSV or Excel format.

4. **Interact with the Data**:
   - View your uploaded data in a table.
   - Ask questions in the query input area (e.g., "Show me the top 10 rows" or "What is the average of column X?").
   - Click "Submit Query" to generate results.

5. **Check Terminal Output**:
   For a detailed response, check your terminal as the agent's responses are also printed there.

## Code Highlights

### File Preprocessing
The `preprocess_and_save` function:
- Detects file type (CSV or Excel).
- Converts date and numeric columns.
- Handles missing values.
- Saves the cleaned data to a temporary file for further use.

### DuckDbAgent Integration
- Utilizes the `DuckDbAgent` from the `phi` library.
- Dynamically configures a semantic model with the uploaded data.
- Responds to queries using the specified model and tools.

### Query Execution
- Users input queries in natural language.
- The agent processes and generates SQL queries to retrieve results.

## Example Queries
- "What is the maximum value in column X?"
- "Show the data where column Y is greater than 50."
- "Find the total count of rows."

## Limitations
- Requires a valid OpenAI API key.
- Only supports CSV and Excel file formats.
- Large datasets may result in slower performance.

## Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Commit your changes and push the branch:
   ```bash
   git commit -m "Add your message here"
   git push origin feature/your-feature-name
   ```
4. Open a pull request.

## License

This project is licensed under the [MIT License](LICENSE). Feel free to use and modify as needed.

## Contact
For any questions or issues, please contact:
- **Name**: [Gowni Amaranatha Reddy]
- **Email**: [amaranthadev@gmail.com]
---

Enjoy analyzing your data efficiently with the Data Analyst Agent!

