"""DuckDB manager for data loading and querying."""

import os
import duckdb
import pandas as pd
from pathlib import Path
from typing import Dict, List, Any, Tuple
import logging

logger = logging.getLogger(__name__)


class DuckDBManager:
    """Manages DuckDB connection and operations."""

    def __init__(self, data_dir: str = None):
        """Initialize DuckDB manager.
        
        Args:
            data_dir: Directory containing CSV files. If None, uses './data'
        """
        self.data_dir = Path(data_dir) if data_dir else Path("./data")
        self.conn = duckdb.connect(":memory:")
        self.loaded_tables = {}
        self._load_csv_files()

    def _load_csv_files(self) -> None:
        """Load all CSV files from data directory into DuckDB."""
        if not self.data_dir.exists():
            logger.warning(f"Data directory {self.data_dir} does not exist")
            return

        csv_files = list(self.data_dir.glob("*.csv"))
        if not csv_files:
            logger.warning(f"No CSV files found in {self.data_dir}")
            return

        for csv_file in csv_files:
            table_name = csv_file.stem  # filename without extension
            try:
                df = pd.read_csv(csv_file)
                self.conn.register(table_name, df)
                self.loaded_tables[table_name] = {
                    "path": str(csv_file),
                    "rows": len(df),
                    "columns": list(df.columns)
                }
                logger.info(f"Loaded table '{table_name}' from {csv_file}")
            except Exception as e:
                logger.error(f"Failed to load {csv_file}: {e}")

    def get_tables(self) -> List[str]:
        """Get list of all available tables.
        
        Returns:
            List of table names
        """
        try:
            result = self.conn.execute("SELECT table_name FROM information_schema.tables WHERE table_type='BASE TABLE'").fetchall()
            return [row[0] for row in result]
        except Exception as e:
            logger.error(f"Error fetching tables: {e}")
            return []

    def get_table_columns(self, table_name: str) -> List[Dict[str, str]]:
        """Get column information for a table.
        
        Args:
            table_name: Name of the table
            
        Returns:
            List of dicts with 'name' and 'type' keys
        """
        try:
            result = self.conn.execute(f"PRAGMA table_info({table_name})").fetchall()
            return [
                {"name": row[1], "type": str(row[2])}
                for row in result
            ]
        except Exception as e:
            logger.error(f"Error fetching columns for {table_name}: {e}")
            return []

    def get_metadata(self) -> Dict[str, Any]:
        """Get complete metadata about all tables and columns.
        
        Returns:
            Dictionary with tables and their column information
        """
        metadata = {}
        tables = self.get_tables()
        
        for table_name in tables:
            columns = self.get_table_columns(table_name)
            metadata[table_name] = {
                "columns": columns,
                "column_names": [col["name"] for col in columns]
            }
        
        return metadata

    def execute_query(self, query: str) -> Tuple[bool, Any]:
        """Execute a SELECT query against DuckDB.
        
        Args:
            query: SQL query to execute
            
        Returns:
            Tuple of (success: bool, result: DataFrame or error message)
        """
        try:
            result = self.conn.execute(query).fetchdf()
            return True, result
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Query execution failed: {error_msg}")
            return False, error_msg

    def get_table_info(self, table_name: str) -> Dict[str, Any]:
        """Get detailed information about a specific table.
        
        Args:
            table_name: Name of the table
            
        Returns:
            Dictionary with table statistics
        """
        try:
            count = self.conn.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
            columns = self.get_table_columns(table_name)
            
            return {
                "name": table_name,
                "row_count": count,
                "column_count": len(columns),
                "columns": columns
            }
        except Exception as e:
            logger.error(f"Error getting table info for {table_name}: {e}")
            return {}

    def reload_data(self) -> None:
        """Reload all CSV files from disk."""
        self.conn.close()
        self.conn = duckdb.connect(":memory:")
        self.loaded_tables.clear()
        self._load_csv_files()
