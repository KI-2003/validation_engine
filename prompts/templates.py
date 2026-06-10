"""Prompt templates for LLM interactions."""

PROMPTS = {
    "sql_generation": """You are a SQL expert assistant. Your task is to convert natural language requests into SQL SELECT queries.

IMPORTANT RULES:
1. Generate ONLY SELECT statements
2. Use ONLY the provided tables and columns below
3. Return ONLY the SQL query, no explanations or markdown
4. Do not add any SQL comments
5. Ensure the query is syntactically correct for DuckDB

Available Tables and Columns:
{schema}

User Request: {user_request}

Generate the SQL query:""",

    "explanation": """You are a data engineering expert. Analyze the following validation results and provide a clear, business-friendly summary.

Validation Results:
{results}

User's Original Request: {original_request}

Provide a concise summary that explains:
1. What was checked
2. Key findings
3. Any issues or anomalies found
4. Recommended actions if needed

Summary:""",

    "metadata_summary": """You are a database analyst. Here's information about the available data:

{metadata}

User Query: {user_query}

Based on the available tables and columns, is this query answerable? Explain briefly what data is available to help answer the user's request."""
}


def get_sql_generation_prompt(schema: str, user_request: str) -> str:
    """Get SQL generation prompt.
    
    Args:
        schema: Database schema information
        user_request: User's natural language request
        
    Returns:
        Formatted prompt
    """
    return PROMPTS["sql_generation"].format(
        schema=schema,
        user_request=user_request
    )


def get_explanation_prompt(results: str, original_request: str) -> str:
    """Get explanation prompt.
    
    Args:
        results: Query results as string
        original_request: Original user request
        
    Returns:
        Formatted prompt
    """
    return PROMPTS["explanation"].format(
        results=results,
        original_request=original_request
    )


def get_metadata_summary_prompt(metadata: str, user_query: str) -> str:
    """Get metadata summary prompt.
    
    Args:
        metadata: Metadata information
        user_query: User's query
        
    Returns:
        Formatted prompt
    """
    return PROMPTS["metadata_summary"].format(
        metadata=metadata,
        user_query=user_query
    )


def format_schema_for_prompt(metadata: dict) -> str:
    """Format database schema metadata for use in prompts.
    
    Args:
        metadata: Database metadata dictionary
        
    Returns:
        Formatted schema string
    """
    schema_lines = []
    
    for table_name, table_info in metadata.items():
        columns = table_info.get("columns", [])
        column_strs = [f"{col['name']} ({col['type']})" for col in columns]
        schema_lines.append(f"Table: {table_name}")
        schema_lines.append(f"  Columns: {', '.join(column_strs)}")
    
    return "\n".join(schema_lines)
