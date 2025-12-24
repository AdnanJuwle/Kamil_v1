import sys
import os

# Fix Windows encoding issues - must be before any imports that use print
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

import gradio as gr
from agent import CodingAgent
from file_ops import save_to_file, execute_file, sanitize_filename
from pathlib import Path

# Initialize the agent
agent = CodingAgent()

# Check if Ollama is available and show warning if not
if not agent._check_ollama_available():
    print("⚠️ Warning: Ollama not found in PATH. Please install Ollama from https://ollama.ai")
    print("   After installation, ensure 'ollama' is in your system PATH.")

def generate_code_ui(instruction: str, context_code: str, context_file_path: str) -> tuple[str, str]:
    """Generate code from instruction with optional context."""
    if not instruction or not instruction.strip():
        return "", "❌ Please provide an instruction."
    
    # Use context file path if provided, otherwise use context code text
    context_file = None
    if context_file_path and context_file_path.strip():
        context_file = context_file_path.strip()
    elif context_code and context_code.strip():
        # If context code is provided but no file path, create a temp context
        # For now, we'll just use the context_code directly in the prompt
        context_file = None
        context_code_text = context_code.strip()
    else:
        context_code_text = ""
    
    # Build prompt with context if provided
    if context_file:
        code, status = agent.generate_code(instruction, context_file)
    elif context_code and context_code.strip():
        # Inject context code directly into prompt
        prompt = f"""You are provided this existing code:
```python
{context_code.strip()}
```

Based on this code, {instruction}"""
        from dataset_utils import replace_known_datasets
        prompt = replace_known_datasets(prompt)
        code, error = agent.call_ollama(prompt)
        if error:
            status = error
        elif code:
            status = "✅ Code generated successfully!"
        else:
            status = "❌ No response received from Ollama."
    else:
        code, status = agent.generate_code(instruction, None)
    
    return code, status

def save_code_ui(code: str, filename: str) -> str:
    """Save generated code to a file."""
    if not code or not code.strip():
        return "❌ No code to save."
    
    if not filename or not filename.strip():
        return "❌ Please provide a filename."
    
    if save_to_file(filename, code):
        return f"✅ Code saved to {filename}"
    else:
        return "❌ Failed to save code."

def run_code_ui(filename: str) -> str:
    """Run a Python file and return output."""
    if not filename or not filename.strip():
        return "❌ Please provide a filename."
    
    sanitized = sanitize_filename(filename)
    if not sanitized:
        return "❌ Invalid filename."
    
    if not os.path.exists(sanitized):
        return f"❌ File '{sanitized}' not found."
    
    import subprocess
    import sys
    
    try:
        result = subprocess.run(
            [sys.executable, sanitized],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            timeout=300
        )
        
        output = ""
        if result.stdout:
            output += f"STDOUT:\n{result.stdout}\n"
        if result.stderr:
            output += f"STDERR:\n{result.stderr}\n"
        if result.returncode != 0:
            output += f"\nExit code: {result.returncode}"
        
        return output if output else "✅ Script executed (no output)"
    except subprocess.TimeoutExpired:
        return "❌ Script execution timed out after 5 minutes."
    except Exception as e:
        return f"❌ Error executing file: {e}"

# Create the Gradio interface
with gr.Blocks(title="AI Coding Assistant") as demo:
    gr.Markdown(
        """
        # 🤖 AI Coding Assistant
        
        Generate Python code using your local Ollama LLM. Enter an instruction and optionally provide context code or a file path.
        """
    )
    
    with gr.Row():
        with gr.Column(scale=2):
            instruction = gr.Textbox(
                label="💡 Instruction",
                placeholder="e.g., Create a function to calculate fibonacci numbers",
                lines=3
            )
            
            with gr.Accordion("📄 Optional Context", open=False):
                context_code = gr.Textbox(
                    label="Paste existing code here",
                    placeholder="Paste your existing code for context...",
                    lines=10
                )
                context_file = gr.Textbox(
                    label="Or provide file path",
                    placeholder="e.g., existing_code.py",
                    lines=1
                )
            
            generate_btn = gr.Button("🚀 Generate Code", variant="primary", size="lg")
            status = gr.Textbox(label="Status", interactive=False)
        
        with gr.Column(scale=3):
            generated_code = gr.Code(
                label="Generated Code",
                language="python",
                lines=20,
                interactive=True
            )
            
            with gr.Row():
                filename_input = gr.Textbox(
                    label="Filename",
                    placeholder="e.g., my_script.py",
                    scale=2
                )
                save_btn = gr.Button("💾 Save", scale=1)
                run_btn = gr.Button("▶️ Run", scale=1)
            
            save_status = gr.Textbox(label="Save Status", interactive=False)
            run_output = gr.Textbox(
                label="Execution Output",
                lines=10,
                interactive=False
            )
    
    # Event handlers
    generate_btn.click(
        fn=generate_code_ui,
        inputs=[instruction, context_code, context_file],
        outputs=[generated_code, status]
    )
    
    save_btn.click(
        fn=save_code_ui,
        inputs=[generated_code, filename_input],
        outputs=[save_status]
    )
    
    run_btn.click(
        fn=run_code_ui,
        inputs=[filename_input],
        outputs=[run_output]
    )
    
    gr.Markdown(
        """
        ### 💡 Tips:
        - Be specific in your instructions for better results
        - Provide context code when modifying existing files
        - Review generated code before saving/running
        - Generated files are saved in the current working directory
        """
    )

if __name__ == "__main__":
    demo.launch(
        share=False, 
        server_name="127.0.0.1", 
        server_port=7860,
        theme=gr.themes.Soft(),
        show_error=True
    )

