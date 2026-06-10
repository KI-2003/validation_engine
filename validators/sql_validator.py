"""SQL query validator using sqlglot."""

import sqlglot
from sqlglot import exp
import logging
from typing import Tuple, List, Dict, Any

logger = logging.getLogger(__name__)


class SQLValidator:
    """Validates SQL queries for safety and correctness."""

    def __init__(self, allowed_tables: List[str] = None):
        """Initialize SQL validator.
        
        Args:
            allowed_tables: List of allowed table names
        """
        self.allowed_tables = set(allowed_tables) if allowed_tables else set()
        self.allowed_columns = {}  # Dict of table_name: [column_names]

    def set_allowed_tables(self, tables: List[str]) -> None:
        """Set the list of allowed tables.
        
        Args:
            tables: List of table names
        """
        self.allowed_tables = set(tables)

    def set_allowed_columns(self, table_columns: Dict[str, List[str]]) -> None:
        """Set the allowed columns for each table.
        
        Args:
            table_columns: Dict mapping table names to list of column names
        """
        self.allowed_columns = {
            table: set(cols) for table, cols in table_columns.items()
        }

    def validate(self, query: str) -> Tuple[bool, str]:
        """Validate a SQL query.
        
        Args:
            query: SQL query to validate
            
        Returns:
            Tuple of (is_valid: bool, message: str)
        """
        # Check if query is empty
        if not query or not query.strip():
            return False, "Query is empty"

        # Try to parse the query
        try:
            parsed = sqlglot.parse_one(query, read="duckdb")
        except Exception as e:
            return False, f"SQL parse error: {str(e)}"

        if not parsed:
            return False, "Failed to parse SQL query"

        # Check if it's a SELECT statement
        if not isinstance(parsed, exp.Select):
            return False, "Only SELECT statements are allowed"

        # Validate tables referenced
        tables = self._extract_tables(parsed)
        if self.allowed_tables:
            invalid_tables = tables - self.allowed_tables
            if invalid_tables:
                return False, f"Unknown tables: {', '.join(invalid_tables)}"

        # Validate columns referenced
        columns_error = self._validate_columns(parsed, tables)
        if columns_error:
            return False, columns_error

        return True, "Query is valid"

    def _extract_tables(self, parsed: exp.Expression) -> set:
        """Extract table names from a parsed SQL expression.
        
        Args:
            parsed: Parsed SQL expression
            
        Returns:
            Set of table names
        """
        tables = set()
        for table in parsed.find_all(exp.Table):
            tables.add(table.name)
        return tables

    def _validate_columns(self, parsed: exp.Expression, tables: set) -> str:
        """Validate that all referenced columns exist in their tables.
        
        Args:
            parsed: Parsed SQL expression
            tables: Set of table names in the query
            
        Returns:
            Error message if validation fails, empty string if valid
        """
        if not self.allowed_columns:
            return ""

        # Get all column references
        for col in parsed.find_all(exp.Column):
            col_name = col.name
            
            # Skip if it's a function or special column
            if col_name.upper() in ("*",):
                continue
            
            # Get the table this column belongs to
            table_name = col.table
            
            if table_name:
                # Column has explicit table reference
                if table_name in self.allowed_columns:
                    if col_name not in self.allowed_columns[table_name]:
                        return f"Unknown column '{col_name}' in table '{table_name}'"
            else:
                # Column without explicit table - must exist in one of the tables
                found = False
                for table in tables:
                    if table in self.allowed_columns:
                        if col_name in self.allowed_columns[table]:
                            found = True
                            break
                
                if not found and tables:
                    valid_tables = [t for t in tables if t in self.allowed_columns]
                    if valid_tables:
                        return f"Column '{col_name}' not found in any table"

        return ""

    def sanitize_query(self, query: str) -> str:
        """Sanitize and format a SQL query.
        
        Args:
            query: SQL query to sanitize
            
        Returns:
            Formatted query
        """
        try:
            parsed = sqlglot.parse_one(query, read="duckdb")
            # Generate formatted SQL
            return parsed.sql(dialect="duckdb")
        except Exception as e:
            logger.warning(f"Failed to sanitize query: {e}")
            return query
