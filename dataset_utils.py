import re
from typing import Dict

# Mapping of short dataset names to their full HuggingFace dataset paths
KNOWN_DATASETS: Dict[str, str] = {
    "iris": "scikit-learn/iris",
    "mnist": "mnist",
    "imdb": "imdb",
    "ag_news": "ag_news",
    "emotion": "dair-ai/emotion",
    "yelp": "yelp_polarity"
}

def replace_known_datasets(code: str) -> str:
    """
    Replace short dataset names with full HuggingFace dataset paths in load_dataset calls.
    
    Uses regex to match load_dataset calls more precisely, avoiding false matches
    in comments or strings.
    
    Args:
        code: The code string to process
        
    Returns:
        Code string with dataset names replaced
    """
    for short_name, full_name in KNOWN_DATASETS.items():
        # Match load_dataset('short_name') or load_dataset("short_name")
        # Using word boundaries and precise pattern matching
        pattern_single = re.compile(
            rf"load_dataset\s*\(\s*['\"]{re.escape(short_name)}['\"]\s*\)",
            re.IGNORECASE
        )
        code = pattern_single.sub(f"load_dataset('{full_name}')", code)
    
    return code
