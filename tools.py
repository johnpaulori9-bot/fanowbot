import os

def write_file(path: str, content: str) -> str:
    """
    Write text content to a file at the given path.
    Overwrites if the file already exists.
    """
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"File written to: {path}"
    except Exception as e:
        return f"Error writing file {path}: {e}"

# -----------------------------
# TOOL A: File Reader
# -----------------------------
def read_file(path):
    if not os.path.exists(path):
        return f"Error: File not found: {path}"
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {e}"


# -----------------------------
# TOOL B: Directory Lister
# -----------------------------
def list_directory(path):
    if not os.path.isdir(path):
        return f"Error: Directory not found: {path}"
    try:
        return "\n".join(os.listdir(path))
    except Exception as e:
        return f"Error listing directory: {e}"


# -----------------------------
# TOOL C: Summarizer
# -----------------------------
def summarize_text(provider, text):
    prompt = f"Summarize the following text:\n\n{text}\n\nSummary:"
    return provider.generate(prompt)
