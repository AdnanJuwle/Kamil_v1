import os

def save_to_file(filename, content):
    with open(filename, "w") as f:
        cleaned = clean_code(content)
        f.write(cleaned)
    print(f"✅ Saved to {filename}")

def execute_file(filename):
    if not os.path.exists(filename):
        print("❌ File not found.")
        return
    os.system(f"python3 {filename}")

def clean_code(raw_output: str) -> str:
    lines = raw_output.strip().splitlines()
    if lines and lines[0].startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].startswith("```"):
        lines = lines[:-1]
    return "\n".join(lines).strip()
