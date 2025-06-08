import subprocess
from file_ops import save_to_file, execute_file
from config import MODEL_NAME
from prompt_templates import SYSTEM_PROMPT
import os
from dataset_utils import replace_known_datasets


class CodingAgent:
    def __init__(self):
        self.memory = {}

    def read_file_content(self, filepath: str) -> str:
        if not os.path.exists(filepath):
            return f"⚠️ Warning: File '{filepath}' not found. Proceeding without file context.\n"
        with open(filepath, 'r') as f:
            return f.read()

    def call_ollama(self, prompt: str) -> str:
        full_prompt = SYSTEM_PROMPT.format(instruction=prompt)
        result = subprocess.run(
            ["ollama", "run", MODEL_NAME, full_prompt],
            capture_output=True,
            text=True,
            timeout=60
        )
        return result.stdout.strip()

    def handle_instruction(self, instruction: str, context_file: str = None) -> str:
        context_code = ""
        if context_file:
            context_code = self.read_file_content(context_file)

        # Build the final prompt with or without file context
        if context_code and not context_code.startswith("⚠️"):
            prompt = f"""You are provided this existing code from `{context_file}`:
```python
{context_code}

Based on this code, {instruction}"""
        else:
            prompt = instruction

        # Postprocess (e.g. replace 'iris' with 'scikit-learn/iris')
        prompt = replace_known_datasets(prompt)

        response = self.call_ollama(prompt)
        return f"🧠 Plan:\n{response}"
