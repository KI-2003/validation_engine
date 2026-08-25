# 🔍 Validation Agent

A local proof-of-concept Streamlit application for data validation using natural language. Powered by Ollama (llama3.1:8b), DuckDB, and modern Python tools.

## Overview

**Validation Agent** enables users to perform data validations entirely through natural language conversations. No cloud APIs required—everything runs locally on your machine.

### Key Features

- 🤖 **Natural Language Queries**: Ask validation questions in plain English
- 📊 **Local Data Processing**: DuckDB for fast data querying
- 🧠 **Local LLM**: Ollama with llama3.1:8b (no API costs)
- ✅ **SQL Validation**: Intelligent SQL validation using sqlglot
- 📈 **Smart Results**: Business-friendly explanations of validation results
- 🚀 **Zero Dependencies**: Runs entirely offline after initial setup

### Data Quality Issues Included

Sample datasets include intentional issues to showcase validation capabilities:

- **customers.csv**: Duplicate customer IDs, missing emails, missing phone numbers
- **transactions.csv**: Negative amounts, null values, zero amounts
- **products.csv**: Clean reference data

## Architecture

```
validation_engine/
├── app.py                 # Main Streamlit application
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── data/                 # CSV files (auto-loaded)
│   ├── customers.csv
│   ├── transactions.csv
│   └── products.csv
├── database/             # DuckDB operations
│   ├── __init__.py
│   └── duckdb_manager.py
├── llm/                  # Ollama integration
│   ├── __init__.py
│   └── ollama_client.py
├── validators/           # SQL validation
│   ├── __init__.py
│   └── sql_validator.py
└── prompts/              # LLM prompt templates
    ├── __init__.py
    └── templates.py
```

## Prerequisites

### System Requirements
- Python 3.8+
- 4GB RAM (minimum)
- ~2GB free disk space for Ollama

### Required Software

1. **Ollama** (for local LLM)
   - Download from: https://ollama.ai
   - Supports: macOS, Linux, Windows (via WSL2)
   - After installation, pull the model:
     ```bash
     ollama pull llama3.1:8b
     ```

2. **Python 3.8+**
   - Check: `python --version`

## Installation

### Step 1: Clone/Setup Repository

```bash
cd validation_engine
```

### Step 2: Create Virtual Environment

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Verify Ollama Setup

```bash
# Check if Ollama is accessible
curl http://localhost:11434/api/tags

# Or use Python to verify
python -c "
from llm import OllamaClient
client = OllamaClient()
if client.check_connection():
    print('✓ Connected to Ollama')
    if client.check_model():
        print('✓ Model llama3.1:8b available')
    else:
        print('✗ Model not found. Run: ollama pull llama3.1:8b')
else:
    print('✗ Cannot connect to Ollama. Is it running?')
"
```

## Quick Start

### 1. Start Ollama Service

In a separate terminal, start Ollama:

```bash
ollama serve
```

You should see output like:
```
2024-01-15 10:30:00 Starting Ollama service
2024-01-15 10:30:01 Listening on http://127.0.0.1:11434
```

### 2. Run the Application

```bash
streamlit run app.py
```

This will:
- Open a browser at `http://localhost:8501`
- Load CSV files from the `data/` folder automatically
- Display available tables in the sidebar
- Show the chat interface for validation requests

### 3. Try Sample Validation Requests

Examples you can try:

```
- Check customer table for duplicate customer IDs
- Find records with missing emails
- Check if transaction amounts are positive
- Count total records in the customers table
- Find customers with null phone numbers
- Get the average transaction amount
- Show transactions with negative amounts
- List all products in the Electronics category
```

## How It Works

### Processing Pipeline

```
User Request
    ↓
[DuckDB Schema Extraction]
    ↓
[LLM SQL Generation]
    ↓
[SQL Validation] ← Uses sqlglot
    ├─ Is it a SELECT?
    ├─ Valid tables?
    └─ Valid columns?
    ↓
[SQL Execution] ← DuckDB query
    ↓
[Results Display]
    ↓
[LLM Explanation Generation]
    ↓
User-Friendly Summary
```

### Key Components

#### 1. Database Manager (`database/duckdb_manager.py`)
- Auto-loads CSV files on startup
- Provides schema metadata
- Executes validated SQL queries
- Returns results as pandas DataFrames

#### 2. Ollama Client (`llm/ollama_client.py`)
- Communicates with local Ollama service
- Generates SQL from natural language
- Creates business-friendly explanations
- Handles connection management

#### 3. SQL Validator (`validators/sql_validator.py`)
- Parses SQL with sqlglot
- Validates table references
- Validates column references
- Rejects non-SELECT statements
- Sanitizes queries

#### 4. Prompt Templates (`prompts/templates.py`)
- SQL generation prompt with schema
- Results explanation prompt
- Metadata summary prompt

## Configuration

### Environment Variables

Create a `.env` file to customize behavior:

```bash
# Ollama configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b

# Application configuration
LOG_LEVEL=INFO
```

### Streamlit Configuration

Streamlit settings are managed in `~/.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#3498db"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#ecf0f1"

[client]
showErrorDetails = true
```

## Troubleshooting

### "Cannot connect to Ollama"

**Issue**: Application shows connection error

**Solutions**:
1. Ensure Ollama is running: `ollama serve`
2. Check Ollama is listening: `curl http://localhost:11434/api/tags`
3. Verify correct URL in `.env` or code

### "Model not found"

**Issue**: Error about llama3.1:8b not available

**Solution**:
```bash
ollama pull llama3.1:8b
# Wait for download to complete (1-2 minutes)
```

### "No CSV files found"

**Issue**: App shows warning about no data

**Solution**:
1. Ensure CSV files are in `data/` folder
2. Check file permissions are readable
3. Verify CSV format (comma-separated)

### SQL Generation Produces Invalid Queries

**Issue**: LLM generates malformed SQL

**Solutions**:
1. Rephrase your request more clearly
2. Try providing specific table names
3. Check database schema sidebar for available tables
4. Reduce prompt complexity

### Slow Response Times

**Issue**: LLM generation takes 30+ seconds

**Solutions**:
1. This is normal for first request (model loads)
2. Ensure adequate system RAM (4GB minimum)
3. Consider using a smaller model if constraints are severe
4. Note: Subsequent requests should be faster

## Adding Custom Data

### Add New CSV Files

1. Create CSV files in `data/` folder
2. Use standard CSV format (headers + comma-separated)
3. Run app again—files auto-load on startup

### Data Format Requirements

- **First row**: Column headers
- **Format**: Comma-separated values
- **Encoding**: UTF-8
- **No special characters** in filenames (use underscores)

Example:
```csv
id,name,value,date
1,John,100,2024-01-01
2,Jane,200,2024-01-02
```

## Advanced Usage

### Modify Prompts

Edit `prompts/templates.py` to customize:
- SQL generation instructions
- Explanation tone
- Validation rules

### Extend Validators

Add custom validation logic to `validators/sql_validator.py`:
- Add table-specific rules
- Implement custom column validation
- Add execution timeout checks

### Scale to Multiple Data Sources

Modify `database/duckdb_manager.py` to:
- Load from databases instead of CSVs
- Support multiple data formats
- Implement caching strategies

## Performance Notes

- **First Run**: ~10-15 seconds (model loads into memory)
- **Subsequent Queries**: ~5-8 seconds (model cached)
- **Query Execution**: <1 second (DuckDB is fast)
- **Result Display**: <2 seconds (Streamlit rendering)

### Optimization Tips

1. **Reduce Dataset Size**: Large CSVs slow down DuckDB loading
2. **Use Indexes**: DuckDB supports indexes for faster queries
3. **Parallel Processing**: Run multiple Ollama instances
4. **GPU Acceleration**: Ollama supports GPU (not enabled by default)

## Security Considerations

⚠️ **This is a proof-of-concept for local use only**

Security features implemented:
- ✓ SQL validation (rejects non-SELECT)
- ✓ Schema validation (only known tables/columns)
- ✓ No external API calls

Not production-ready for:
- Multi-user environments
- Sensitive data exposure
- Network-exposed instances

## Limitations

1. **Model Limitations**: llama3.1:8b occasionally generates invalid SQL
   - Workaround: Rephrase requests

2. **Complex Queries**: LLM struggles with multi-table joins
   - Workaround: Break into multiple simpler requests

3. **Performance**: Larger datasets (100K+ rows) may be slow
   - Solution: Filter data or use database views

4. **Error Messages**: Some DuckDB errors are cryptic
   - Solution: Check SQL in the expanded "Generated SQL" section

## Extending the System

### Add Custom Validators

```python
# In validators/sql_validator.py
def validate_performance(self, query: str) -> Tuple[bool, str]:
    # Check query complexity
    # Reject queries with too many joins
    pass
```

### Add Custom LLM Providers

```python
# Create new file: llm/provider_base.py
class LLMProvider:
    def generate_sql(self, prompt: str) -> str:
        pass
```

### Add More LLM Capabilities

```python
# In llm/ollama_client.py
def generate_summary_statistics(self, data: pd.DataFrame) -> str:
    # Generate statistical summaries
    pass
```

## Development

### Running Tests

```bash
pytest tests/ -v
```

### Code Style

```bash
# Format code
black .

# Lint
flake8 .

# Type checking
mypy .
```

### Debugging

Enable debug logging:

```bash
# In terminal
export LOG_LEVEL=DEBUG

# Or in .env
LOG_LEVEL=DEBUG
```

## Project Structure Philosophy

- **Modular**: Each component has single responsibility
- **Configurable**: Environment variables for customization
- **Testable**: Functions are pure and deterministic
- **Documented**: Docstrings for all functions
- **Scalable**: Can be extended without breaking existing code

## License

This project is provided as-is for educational and research purposes.

## Contributing

To improve this project:

1. Report bugs or request features via GitHub issues
2. Submit pull requests for improvements
3. Add tests for new functionality
4. Update documentation

## Resources

- **Ollama Documentation**: https://ollama.ai/docs
- **DuckDB Guide**: https://duckdb.org/docs
- **Streamlit Docs**: https://docs.streamlit.io
- **sqlglot Reference**: https://github.com/tobymao/sqlglot

## Support

For issues or questions:

1. Check troubleshooting section above
2. Review generated SQL (expand SQL section)
3. Check Ollama logs: `ollama logs`
4. Verify CSV data format

## Next Steps

### To enhance this project:

1. **Add authentication**: User login/session management
2. **Add persistence**: Save validation histories
3. **Add scheduling**: Schedule regular validations
4. **Add alerts**: Notify on data quality issues
5. **Add metrics**: Track query success rates
6. **Add export**: CSV/PDF export of results
7. **Add collaboration**: Multi-user support
8. **Add ML**: Learn from validation patterns

---

**Happy Validating! 🚀**



<img width="1920" height="836" alt="Screenshot 2026-08-25 at 19-59-36 Validation Agent" src="https://github.com/user-attachments/assets/e8375706-32f4-4097-b56d-58116e0e86d0" />

<img width="1920" height="836" alt="Screenshot 2026-08-25 at 20-00-43 Validation Agent" src="https://github.com/user-attachments/assets/ab37fa60-c83c-4763-b589-581c32fad2c7" />

<img width="1920" height="836" alt="Screenshot 2026-08-25 at 20-01-11 Validation Agent" src="https://github.com/user-attachments/assets/4e331bd4-4903-4d79-99c4-2e009c15d261" />

<img width="1920" height="836" alt="Screenshot 2026-08-25 at 20-01-58 Validation Agent" src="https://github.com/user-attachments/assets/79941e40-509f-479e-9f99-2add67053473" />


