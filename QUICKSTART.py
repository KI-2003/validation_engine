"""
Quick start guide for Validation Engine
"""

SETUP_INSTRUCTIONS = """
╔════════════════════════════════════════════════════════════════════════╗
║                  🔍 VALIDATION ENGINE - QUICK START                    ║
╚════════════════════════════════════════════════════════════════════════╝

STEP 1: Install Prerequisites
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Install Python 3.8+ (if not already installed)
   https://www.python.org/downloads/

2. Install Ollama from: https://ollama.ai
   
   After installation, download the model:
   > ollama pull llama3.1:8b
   
   (This takes 2-5 minutes depending on connection)

STEP 2: Set Up Virtual Environment
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Windows:
  > python -m venv .venv
  > .venv\\Scripts\\activate

macOS/Linux:
  $ python3 -m venv .venv
  $ source .venv/bin/activate

You should see (.venv) in your prompt.

STEP 3: Install Dependencies
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  > pip install -r requirements.txt

STEP 4: Start the Application
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Terminal 1 (Start Ollama service):
  > ollama serve

Terminal 2 (From validation_engine folder):
  > python run.py

STEP 5: Use the Application
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Your browser should open to: http://localhost:8501

Try these sample requests:
  • "Check for duplicate customer IDs"
  • "Find records with missing emails"
  • "Show transactions with negative amounts"
  • "Count the total number of customers"

TROUBLESHOOTING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Q: "Cannot connect to Ollama"
A: Make sure you ran "ollama serve" in another terminal

Q: "Model not found"
A: Run "ollama pull llama3.1:8b" and wait for it to complete

Q: "ModuleNotFoundError"
A: Make sure your virtual environment is activated
   and you ran "pip install -r requirements.txt"

Q: "No CSV files found"
A: CSV files should be in the 'data/' folder
   Three sample files are already included

PROJECT STRUCTURE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

validation_engine/
├── app.py                 # Main application
├── config.py             # Configuration
├── run.py                # Quick start script
├── requirements.txt      # Python packages
├── README.md             # Full documentation
├── data/                 # CSV files (auto-loaded)
├── database/             # DuckDB functions
├── llm/                  # Ollama integration
├── validators/           # SQL validation
└── prompts/              # LLM prompts

KEY FILES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

database/duckdb_manager.py
  - Loads CSV files
  - Executes SQL queries
  - Returns results

llm/ollama_client.py
  - Communicates with Ollama
  - Generates SQL from natural language
  - Creates explanations

validators/sql_validator.py
  - Validates SQL safety
  - Checks table/column references

prompts/templates.py
  - Customizable LLM prompts

EXAMPLE WORKFLOW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. User: "Find duplicate customer IDs"
2. System: Fetches database schema
3. System: Asks LLM to write SQL
4. System: Validates the SQL query
5. System: Executes query on DuckDB
6. System: Shows results to user
7. System: Uses LLM to explain findings

ADDING YOUR OWN DATA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Create CSV files in the data/ folder
2. Restart the application (it auto-loads CSV files)
3. Your tables will appear in the sidebar

CSV Format:
  - First row: column names
  - Comma-separated values
  - UTF-8 encoding
  - No special characters in filenames

NEXT STEPS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

See README.md for:
  - Complete documentation
  - Advanced configuration
  - Performance optimization
  - Extending the system
  - Troubleshooting guide

SUPPORT & RESOURCES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Ollama: https://ollama.ai/docs
DuckDB: https://duckdb.org/docs
Streamlit: https://docs.streamlit.io
sqlglot: https://github.com/tobymao/sqlglot

═══════════════════════════════════════════════════════════════════════════

Happy Validating! 🚀
"""

if __name__ == "__main__":
    print(SETUP_INSTRUCTIONS)
