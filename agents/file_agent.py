class Agent:
    def __init__(self):
        pass

    def summarize_file(self, filename):
        try:
            with open(filename, "r") as f:
                lines = f.readlines()
            # Return the first 5 lines as a "summary"
            summary = "".join(lines[:5])
            return summary.strip()
        except FileNotFoundError:
            return f"File {filename} not found."
        except Exception as e:
            return f"Error reading {filename}: {e}"
