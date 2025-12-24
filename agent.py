import subprocess
import os
import sys
import shutil

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
from file_ops import save_to_file, execute_file, sanitize_filename
from config import MODEL_NAME, TIMEOUT_SECONDS
from prompt_templates import SYSTEM_PROMPT
from dataset_utils import replace_known_datasets

class CodingAgent:
    """AI coding assistant that uses local Ollama LLM for code generation."""
    
    def __init__(self):
        """Initialize the coding agent."""
        self._check_ollama_available()
    
    def _check_ollama_available(self) -> bool:
        """Check if Ollama is available in the system."""
        import shutil
        ollama_path = shutil.which("ollama")
        if ollama_path:
            return True
        
        # Check common Windows installation paths
        if sys.platform == 'win32':
            common_paths = [
                os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Programs', 'Ollama', 'ollama.exe'),
                os.path.join(os.environ.get('ProgramFiles', ''), 'Ollama', 'ollama.exe'),
            ]
            for path in common_paths:
                if path and os.path.exists(path):
                    return True
        
        return False

    def read_file_content(self, filepath: str) -> str:
        """Read file content with proper error handling and encoding."""
        try:
            # Sanitize path to prevent directory traversal
            path = Path(filepath)
            if not path.is_absolute():
                path = Path.cwd() / path
            
            # Resolve to prevent .. attacks
            path = path.resolve()
            
            # Ensure file is within current directory or subdirectories
            if not str(path).startswith(str(Path.cwd().resolve())):
                print(f"⚠️ Warning: File path outside working directory. Access denied.")
                return ""
            
            if not path.exists():
                print(f"⚠️ Warning: File '{filepath}' not found. Proceeding without file context.")
                return ""
            
            if not path.is_file():
                print(f"⚠️ Warning: '{filepath}' is not a file. Proceeding without file context.")
                return ""
            
            # Try UTF-8 first, then fallback to other encodings
            try:
                with open(path, 'r', encoding='utf-8', errors='replace') as f:
                    return f.read()
            except UnicodeDecodeError:
                # Fallback to latin-1 which can read any byte sequence
                try:
                    with open(path, 'r', encoding='latin-1', errors='replace') as f:
                        return f.read()
                except Exception:
                    print(f"⚠️ Warning: Could not decode '{filepath}'. Proceeding without file context.")
                    return ""
        except PermissionError:
            print(f"⚠️ Warning: Permission denied reading '{filepath}'. Proceeding without file context.")
            return ""
        except Exception as e:
            print(f"⚠️ Warning: Error reading file '{filepath}': {e}. Proceeding without file context.")
            return ""

    def _get_ollama_path(self) -> str:
        """Get the path to Ollama executable."""
        # First try to find it in PATH
        ollama_path = shutil.which("ollama")
        if ollama_path:
            return ollama_path
        
        # Check common Windows installation paths
        if sys.platform == 'win32':
            common_paths = [
                os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Programs', 'Ollama', 'ollama.exe'),
                os.path.join(os.environ.get('ProgramFiles', ''), 'Ollama', 'ollama.exe'),
            ]
            for path in common_paths:
                if path and os.path.exists(path):
                    return path
        
        return "ollama"  # Fallback to just "ollama" and let subprocess handle the error
    
    def call_ollama(self, prompt: str) -> tuple[str, str]:
        """
        Call Ollama API with proper error handling.
        
        Returns:
            tuple: (response, error_message) where response is the code or empty string, and error_message is any error
        """
        try:
            ollama_path = self._get_ollama_path()
            full_prompt = SYSTEM_PROMPT.format(instruction=prompt)
            result = subprocess.run(
                [ollama_path, "run", MODEL_NAME, full_prompt],
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace',
                timeout=TIMEOUT_SECONDS
            )
            
            if result.returncode != 0:
                error_msg = result.stderr.strip() if result.stderr else "Unknown error"
                return "", f"❌ Ollama error (code {result.returncode}): {error_msg}"
            
            output = result.stdout.strip()
            if not output:
                return "", "❌ Ollama returned empty response. The model might not be loaded. Try: ollama pull " + MODEL_NAME
            
            return output, ""
        except subprocess.TimeoutExpired:
            return "", f"❌ Ollama request timed out after {TIMEOUT_SECONDS} seconds."
        except FileNotFoundError:
            return "", "❌ Error: 'ollama' command not found. Please install Ollama from https://ollama.ai and ensure it's in your PATH."
        except Exception as e:
            return "", f"❌ Unexpected error calling Ollama: {str(e)}"

    def generate_code(self, instruction: str, context_file: Optional[str] = None) -> tuple[str, str]:
        """
        Generate code from instruction and return the result.
        
        Returns:
            tuple: (code, status_message) where code is the generated code and status_message is any error/info
        """
        if not instruction or not instruction.strip():
            return "", "❌ Empty instruction provided."
        
        context_code = ""
        if context_file and context_file.strip():
            context_code = self.read_file_content(context_file.strip())

        # Build the final prompt, inject file content if present
        if context_code:
            prompt = f"""You are provided this existing code from {context_file}:
```python
{context_code}
```

Based on this code, {instruction}"""
        else:
            prompt = instruction

        # Apply dataset replacements
        prompt = replace_known_datasets(prompt)

        response, error = self.call_ollama(prompt)
        
        if error:
            return "", error
        
        if not response:
            return "", "❌ No response received from Ollama. Please try again."
        
        return response, "✅ Code generated successfully!"

    def handle_instruction(self, instruction: str, context_file: Optional[str] = None) -> None:
        """Handle a coding instruction from the user (CLI version)."""
        if not instruction or not instruction.strip():
            print("❌ Empty instruction provided.")
            return
        
        print("🤖 Thinking...")

        code, status = self.generate_code(instruction, context_file)
        
        if not code:
            print(status)
            return
        
        print("\n🧠 Plan:\n" + code)

        save = input("💾 Save to file? (y/n): ").lower().strip()
        if save == "y":
            filename = input("📄 Filename (e.g., tool.py): ").strip()
            if filename:
                if save_to_file(filename, code):
                    run = input("▶️ Run this file? (y/n): ").lower().strip()
                    if run == "y":
                        # Use sanitized filename from save_to_file
                        sanitized = sanitize_filename(filename)
                        if sanitized:
                            execute_file(sanitized)
            else:
                print("❌ No filename provided.")
