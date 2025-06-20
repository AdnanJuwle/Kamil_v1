import subprocess
from file_ops import save_to_file, execute_file
from config import MODEL_NAME
from config import TIMEOUT_SECONDS
from prompt_templates import SYSTEM_PROMPT
import os
from dataset_utils import replace_known_datasets

class CodingAgent:
    def __init__(self):
        self.memory = {}

    def read_file_content(self, filepath: str) -> str:
        if not os.path.exists(filepath):
            print(f"⚠️ Warning: File '{filepath}' not found. Proceeding without file context.")
            return ""
        with open(filepath, 'r') as f:
            return f.read()

    def call_ollama(self, prompt: str) -> str:
        full_prompt = SYSTEM_PROMPT.format(instruction=prompt)
        result = subprocess.run(
            ["ollama", "run", MODEL_NAME, full_prompt],
            capture_output=True,
            text=True,
            timeout=TIMEOUT_SECONDS
        )
        return result.stdout.strip()

    def handle_instruction(self, instruction: str, context_file: str = None):
        print("🤖 Thinking...")

        context_code = ""
        if context_file:
            context_code = self.read_file_content(context_file)

        # Build the final prompt, inject file content if present
        if context_code:
            prompt = f"""You are provided this existing code from {context_file}:
        ```python
        {context_code}

        Based on this code, {instruction}"""
        else:
            prompt = instruction

        # Optionally apply dataset replacements or any postprocessing here
        prompt = replace_known_datasets(prompt)

        response = self.call_ollama(prompt)
        print("\n🧠 Plan:\n" + response)

        save = input("💾 Save to file? (y/n): ").lower()
        if save == "y":
            filename = input("📄 Filename (e.g., tool.py): ").strip()
            save_to_file(filename, response)
            run = input("▶️ Run this file? (y/n): ").lower()
            if run == "y":
                execute_file(filename)
