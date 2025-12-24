import os
from typing import Optional

# Default configuration values
DEFAULT_MODEL_NAME = "mistral:latest"
DEFAULT_TIMEOUT_SECONDS = 300

# Configuration with environment variable support
MODEL_NAME: str = os.getenv("OLLAMA_MODEL", DEFAULT_MODEL_NAME)
TIMEOUT_SECONDS: int = int(os.getenv("OLLAMA_TIMEOUT", str(DEFAULT_TIMEOUT_SECONDS)))

# Validation
if TIMEOUT_SECONDS <= 0:
    raise ValueError("TIMEOUT_SECONDS must be a positive integer")

if not MODEL_NAME or not MODEL_NAME.strip():
    raise ValueError("MODEL_NAME cannot be empty")
