"""Main Streamlit application for Validation Agent."""

import streamlit as st
import logging
import json
from typing import Optional
from pathlib import Path

from database import DuckDBManager
from llm import OllamaClient
from validators import SQLValidator
from prompts import PROMPTS
from prompts.templates import (
    format_schema_for_prompt,
    get_sql_generation_prompt,
    get_explanation_prompt
)
from config import (
    DATA_DIR,
    OLLAMA_BASE_URL,
    OLLAMA_MODEL,
    LOG_LEVEL,
    MAX_RESULTS_DISPLAY
)

# Configure logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="Validation Agent",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Streamlit theming
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)


@st.cache_resource
def initialize_database():
    """Initialize and cache the database manager."""
    logger.info(f"Initializing database from {DATA_DIR}")
    return DuckDBManager(data_dir=str(DATA_DIR))


@st.cache_resource
def initialize_ollama():
    """Initialize and cache the Ollama client."""
    logger.info(f"Initializing Ollama client at {OLLAMA_BASE_URL}")
    return OllamaClient(base_url=OLLAMA_BASE_URL, model=OLLAMA_MODEL)


@st.cache_resource
def initialize_validator():
    """Initialize and cache the SQL validator."""
    logger.info("Initializing SQL validator")
    return SQLValidator()


def check_ollama_connection() -> bool:
    """Check if Ollama is running and model is available."""
    ollama = initialize_ollama()
    
    if not ollama.check_connection():
        st.error(f"❌ Cannot connect to Ollama at {OLLAMA_BASE_URL}")
        st.info("Please ensure Ollama is running. You can start it with: `ollama serve`")
        return False
    
    if not ollama.check_model():
        st.error(f"❌ Model '{OLLAMA_MODEL}' not found in Ollama")
        st.info(f"Please pull the model first with: `ollama pull {OLLAMA_MODEL}`")
        return False
    
    return True


def display_table_info():
    """Display information about available tables in sidebar."""
    db = initialize_database()
    tables = db.get_tables()
    
    with st.sidebar:
        st.subheader("📊 Available Tables")
        
        if not tables:
            st.warning("No tables loaded. Please ensure CSV files are in the 'data' folder.")
            return
        
        for table_name in tables:
            with st.expander(f"📋 {table_name}"):
                table_info = db.get_table_info(table_name)
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Rows", f"{table_info.get('row_count', 0):,}")
                with col2:
                    st.metric("Columns", table_info.get("column_count", 0))
                
                st.write("**Columns:**")
                for col in table_info.get("columns", []):
                    st.text(f"  • {col['name']} ({col['type']})")


def process_validation_request(user_request: str) -> dict:
    """Process a validation request end-to-end.
    
    Args:
        user_request: Natural language request from user
        
    Returns:
        Dictionary with results
    """
    db = initialize_database()
    ollama = initialize_ollama()
    validator = initialize_validator()
    
    result = {
        "success": False,
        "query": None,
        "validation_error": None,
        "execution_error": None,
        "data": None,
        "explanation": None
    }
    
    try:
        # Step 1: Get database metadata
        with st.status("📊 Retrieving database schema...", expanded=False):
            metadata = db.get_metadata()
            schema_text = format_schema_for_prompt(metadata)
            
            # Update validator with allowed tables and columns
            validator.set_allowed_tables(list(metadata.keys()))
            table_columns = {
                table: [col["name"] for col in info["columns"]]
                for table, info in metadata.items()
            }
            validator.set_allowed_columns(table_columns)
            st.write("✓ Schema loaded")
        
        # Step 2: Generate SQL using LLM
        with st.status("🤖 Generating SQL query...", expanded=False):
            prompt = get_sql_generation_prompt(schema_text, user_request)
            generated_sql = ollama.generate_sql(prompt)
            
            if not generated_sql:
                result["execution_error"] = "Failed to generate SQL from LLM"
                return result
            
            result["query"] = generated_sql
            st.write(f"Generated: `{generated_sql}`")
        
        # Step 3: Validate SQL
        with st.status("✅ Validating SQL query...", expanded=False):
            is_valid, validation_msg = validator.validate(generated_sql)
            
            if not is_valid:
                result["validation_error"] = validation_msg
                st.error(f"Validation failed: {validation_msg}")
                return result
            
            st.write("✓ Query is valid")
        
        # Step 4: Execute SQL
        with st.status("⚙️ Executing query...", expanded=False):
            success, exec_result = db.execute_query(generated_sql)
            
            if not success:
                result["execution_error"] = str(exec_result)
                st.error(f"Execution failed: {exec_result}")
                return result
            
            result["data"] = exec_result
            st.write(f"✓ Returned {len(exec_result)} rows")
        
        # Step 5: Generate explanation
        with st.status("💬 Generating explanation...", expanded=False):
            results_str = exec_result.to_string() if len(exec_result) > 0 else "No results"
            explanation_prompt = get_explanation_prompt(results_str, user_request)
            explanation = ollama.generate_explanation(explanation_prompt)
            
            if explanation:
                result["explanation"] = explanation
                st.write("✓ Explanation generated")
        
        result["success"] = True
        
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        result["execution_error"] = str(e)
    
    return result


def main():
    """Main Streamlit application."""
    # Header
    st.title("🔍 Validation Agent")
    st.markdown("_Data Validation through Natural Language_")
    
    # Check prerequisites
    if not DATA_DIR.exists():
        st.warning(f"⚠️ Data directory not found: {DATA_DIR}")
        st.info("Please create a 'data' folder with CSV files to validate.")
        return
    
    # Initialize database
    db = initialize_database()
    tables = db.get_tables()
    
    if not tables:
        st.warning("⚠️ No CSV files found in the data folder.")
        st.info("Please add CSV files to the 'data' folder to get started.")
        return
    
    # Check Ollama connection
    if not check_ollama_connection():
        return
    
    # Display available tables in sidebar
    display_table_info()
    
    # Main content
    st.subheader("💬 Ask Validation Questions")
    
    # Example requests
    with st.expander("📝 Example Validation Requests"):
        st.markdown("""
        - Check customer table for duplicate customer IDs
        - Find records with missing emails
        - Check if transaction amounts are positive
        - Count total records in the customers table
        - Find customers with invalid email formats
        - Get average transaction amount per customer
        - Check for records with null values in critical columns
        """)
    
    # User input
    user_request = st.text_input(
        "Enter your validation request:",
        placeholder="e.g., Check for duplicate customer IDs in the customers table",
        key="user_request"
    )
    
    if user_request:
        st.divider()
        
        # Process the request
        result = process_validation_request(user_request)
        
        # Display results
        if result["success"]:
            st.success("✅ Validation completed successfully!")
            
            # Display generated SQL
            with st.expander("📋 Generated SQL Query"):
                st.code(result["query"], language="sql")
            
            # Display data results
            if result["data"] is not None and len(result["data"]) > 0:
                st.subheader("📊 Results")
                
                # Display with pagination if needed
                if len(result["data"]) > MAX_RESULTS_DISPLAY:
                    st.warning(f"Showing first {MAX_RESULTS_DISPLAY} of {len(result['data'])} rows")
                    st.dataframe(result["data"].head(MAX_RESULTS_DISPLAY), use_container_width=True)
                else:
                    st.dataframe(result["data"], use_container_width=True)
            else:
                st.info("Query returned no results.")
            
            # Display explanation
            if result["explanation"]:
                st.subheader("💡 Analysis")
                st.markdown(result["explanation"])
        else:
            # Display error information
            st.error("❌ Validation request failed")
            
            if result["query"]:
                st.write("**Generated SQL:**")
                st.code(result["query"], language="sql")
            
            if result["validation_error"]:
                st.error(f"**Validation Error:** {result['validation_error']}")
            
            if result["execution_error"]:
                st.error(f"**Execution Error:** {result['execution_error']}")


if __name__ == "__main__":
    main()
