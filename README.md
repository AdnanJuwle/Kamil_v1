# AI Coding Assistant

A local LLM-powered coding assistant that helps you generate Python code using Ollama. This is a command-line tool that uses a local language model to generate, modify, and execute Python code.

## Features

- 🤖 **Local LLM Integration**: Uses Ollama for private, local code generation
- 📝 **Code Generation**: Generate Python code from natural language instructions
- 📄 **File Context**: Provide existing code files as context for modifications
- 💾 **Save & Execute**: Save generated code and optionally run it immediately
- 🔒 **Security**: Input validation and path sanitization to prevent security issues
- 🪟 **Cross-Platform**: Works on Windows, macOS, and Linux

## Prerequisites

1. **Python 3.7+** installed on your system
2. **Ollama** installed and configured
   - Download from: https://ollama.ai
   - Ensure the `ollama` command is in your system PATH
   - Pull a model (default: `mistral:latest`):
     ```bash
     ollama pull mistral:latest
     ```

## Installation

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd Kamil_v1
   ```

2. No additional Python packages are required (uses only standard library)

3. Verify Ollama is working:
   ```bash
   ollama list
   ```

## Configuration

You can configure the assistant using environment variables:

- `OLLAMA_MODEL`: The Ollama model to use (default: `mistral:latest`)
- `OLLAMA_TIMEOUT`: Timeout in seconds for Ollama requests (default: `300`)

Example:
```bash
# Linux/macOS
export OLLAMA_MODEL="llama2:latest"
export OLLAMA_TIMEOUT=600

# Windows PowerShell
$env:OLLAMA_MODEL="llama2:latest"
$env:OLLAMA_TIMEOUT=600
```

Or edit `config.py` directly to change defaults.

## Usage

Run the assistant:
```bash
python main.py
```

### Basic Workflow

1. Enter your coding instruction when prompted:
   ```
   You: create a function to calculate fibonacci numbers
   ```

2. Optionally provide a file for context:
   ```
   Do you want to provide a file for context? (y/n): y
   Enter file path: existing_code.py
   ```

3. Review the generated code

4. Save to file (optional):
   ```
   💾 Save to file? (y/n): y
   📄 Filename (e.g., tool.py): fibonacci.py
   ```

5. Run the file (optional):
   ```
   ▶️ Run this file? (y/n): y
   ```

### Example Session

```
📎 AI Coding Assistant (type 'exit' or 'quit' to quit)

You: make a calculator python script
Do you want to provide a file for context? (y/n): n
🤖 Thinking...

🧠 Plan:
def calculate(operation, num1, num2):
    if operation == '+':
        return num1 + num2
    elif operation == '-':
        return num1 - num2
    elif operation == '*':
        return num1 * num2
    elif operation == '/':
        return num1 / num2
    else:
        raise ValueError('Invalid operation')

💾 Save to file? (y/n): y
📄 Filename (e.g., tool.py): calculator.py
✅ Saved to calculator.py
▶️ Run this file? (y/n): n
```

## Dataset Support

The assistant automatically replaces common dataset names with their full HuggingFace paths:
- `iris` → `scikit-learn/iris`
- `mnist` → `mnist`
- `imdb` → `imdb`
- `ag_news` → `ag_news`
- `emotion` → `dair-ai/emotion`
- `yelp` → `yelp_polarity`

## Project Structure

```
Kamil_v1/
├── main.py              # Entry point
├── agent.py             # CodingAgent class
├── config.py            # Configuration settings
├── file_ops.py          # File operations (save, execute)
├── dataset_utils.py     # Dataset name replacements
├── prompt_templates.py  # LLM prompt templates
├── requirements.txt     # Dependencies (none required)
├── README.md           # This file
└── testresults/        # Generated test files
```

## Security Features

- **Path Sanitization**: Prevents directory traversal attacks
- **Input Validation**: Validates all user inputs
- **Safe Execution**: Uses subprocess instead of os.system
- **File Encoding**: Explicit UTF-8 encoding for cross-platform compatibility

## Troubleshooting

### "ollama command not found"
- Ensure Ollama is installed and in your PATH
- Verify with: `ollama --version`

### "Model not found"
- Pull the model: `ollama pull mistral:latest`
- Or change `MODEL_NAME` in `config.py`

### Timeout errors
- Increase `TIMEOUT_SECONDS` in `config.py` or set `OLLAMA_TIMEOUT` environment variable
- Check if your model is too slow for your hardware

### Permission errors
- Ensure you have write permissions in the current directory
- Check file paths are valid and accessible

## Contributing

This is an early version. Contributions and improvements are welcome!

## License

[Add your license here]

## Notes

- This is the first version (v1) - expect rough edges
- The assistant generates code but doesn't guarantee correctness
- Always review generated code before using in production
- Generated files are saved in the current working directory

