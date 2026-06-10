"""Ollama client for LLM interactions."""

import requests
import logging
from typing import Optional, Dict, Any
import json

logger = logging.getLogger(__name__)


class OllamaClient:
    """Client for interacting with Ollama API."""

    def __init__(self, base_url: str = "http://localhost:11434", model: str = "llama3.1:8b"):
        """Initialize Ollama client.
        
        Args:
            base_url: Base URL for Ollama API
            model: Model name to use
        """
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.api_endpoint = f"{self.base_url}/api/generate"
        self.health_endpoint = f"{self.base_url}/api/tags"

    def check_connection(self) -> bool:
        """Check if Ollama is running and accessible.
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            response = requests.get(self.health_endpoint, timeout=5)
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Failed to connect to Ollama: {e}")
            return False

    def check_model(self) -> bool:
        """Check if the specified model is available.
        
        Returns:
            True if model is available, False otherwise
        """
        try:
            response = requests.get(self.health_endpoint, timeout=5)
            if response.status_code != 200:
                return False
            
            models = response.json().get("models", [])
            model_names = [m.get("name") for m in models]
            
            # Check if model is available (exact match or with tag)
            return any(self.model in name for name in model_names)
        except Exception as e:
            logger.error(f"Failed to check model availability: {e}")
            return False

    def generate(self, prompt: str, temperature: float = 0.3, top_p: float = 0.9) -> Optional[str]:
        """Generate response using Ollama.
        
        Args:
            prompt: Input prompt
            temperature: Creativity level (0-1)
            top_p: Diversity parameter (0-1)
            
        Returns:
            Generated text or None if error
        """
        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "temperature": temperature,
                "top_p": top_p,
            }
            
            response = requests.post(self.api_endpoint, json=payload, timeout=60)
            response.raise_for_status()
            
            result = response.json()
            return result.get("response", "").strip()
        except requests.exceptions.Timeout:
            logger.error("Ollama request timed out")
            return None
        except Exception as e:
            logger.error(f"Error generating with Ollama: {e}")
            return None

    def generate_sql(self, prompt: str) -> Optional[str]:
        """Generate SQL query using Ollama.
        
        Args:
            prompt: Prompt with context and schema
            
        Returns:
            Generated SQL query or None if error
        """
        try:
            response = self.generate(prompt, temperature=0.1)  # Lower temperature for SQL
            
            if not response:
                return None
            
            # Extract SQL from response (handle cases with markdown code blocks)
            response = response.strip()
            
            # Remove markdown code blocks if present
            if "```sql" in response:
                response = response.split("```sql")[1].split("```")[0].strip()
            elif "```" in response:
                response = response.split("```")[1].split("```")[0].strip()
            
            # Remove any leading/trailing whitespace
            response = response.strip()
            
            # Ensure it's a SELECT statement only
            if not response.upper().startswith("SELECT"):
                logger.warning(f"Generated query doesn't start with SELECT: {response}")
                return None
            
            return response
        except Exception as e:
            logger.error(f"Error generating SQL: {e}")
            return None

    def generate_explanation(self, prompt: str) -> Optional[str]:
        """Generate business-friendly explanation using Ollama.
        
        Args:
            prompt: Prompt with results to explain
            
        Returns:
            Generated explanation or None if error
        """
        try:
            response = self.generate(prompt, temperature=0.5)
            return response
        except Exception as e:
            logger.error(f"Error generating explanation: {e}")
            return None
