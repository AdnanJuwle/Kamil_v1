import os
import subprocess
import sys

# Fix Windows encoding issues - must be before any print statements
if sys.platform == 'win32':
    import io
    try:
        # Check if we need to fix encoding (not already UTF-8)
        if hasattr(sys.stdout, 'buffer') and getattr(sys.stdout, 'encoding', '').lower() != 'utf-8':
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace', line_buffering=True)
    except (AttributeError, ValueError, TypeError):
        pass
    try:
        if hasattr(sys.stderr, 'buffer') and getattr(sys.stderr, 'encoding', '').lower() != 'utf-8':
            sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace', line_buffering=True)
    except (AttributeError, ValueError, TypeError):
        pass

from pathlib import Path
from typing import Optional

def clean_code(raw_output: str) -> str:
    """Remove markdown code blocks from raw output."""
    lines = raw_output.strip().splitlines()
    if lines and lines[0].startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].startswith("```"):
        lines = lines[:-1]
    return "\n".join(lines).strip()

def sanitize_filename(filename: str) -> Optional[str]:
    """Sanitize filename to prevent path traversal attacks."""
    if not filename or not filename.strip():
        return None
    
    # Remove any path components
    filename = os.path.basename(filename.strip())
    
    # Remove any invalid characters
    invalid_chars = '<>:"|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    
    # Ensure it's a Python file
    if not filename.endswith('.py'):
        filename += '.py'
    
    return filename

def save_to_file(filename: str, content: str) -> bool:
    """Save content to a file with proper error handling."""
    try:
        sanitized = sanitize_filename(filename)
        if not sanitized:
            print("❌ Invalid filename provided.")
            return False
        
        # Ensure we're saving in the current directory or a safe subdirectory
        filepath = Path(sanitized)
        if filepath.is_absolute() or '..' in str(filepath):
            print("❌ Invalid file path. Please use a simple filename.")
            return False
        
        with open(filepath, "w", encoding="utf-8") as f:
            cleaned = clean_code(content)
            f.write(cleaned)
        print(f"✅ Saved to {filepath}")
        return True
    except PermissionError:
        print(f"❌ Permission denied: Cannot write to {filename}")
        return False
    except OSError as e:
        print(f"❌ Error saving file: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def execute_file(filename: str) -> bool:
    """Execute a Python file using subprocess with proper error handling."""
    try:
        if not os.path.exists(filename):
            print("❌ File not found.")
            return False
        
        # Use sys.executable for cross-platform compatibility
        result = subprocess.run(
            [sys.executable, filename],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            timeout=300  # 5 minute timeout
        )
        
        if result.stdout:
            print(result.stdout)
        
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        
        if result.returncode != 0:
            print(f"❌ Script exited with code {result.returncode}")
            return False
        
        return True
    except subprocess.TimeoutExpired:
        print("❌ Script execution timed out after 5 minutes.")
        return False
    except Exception as e:
        print(f"❌ Error executing file: {e}")
        return False
