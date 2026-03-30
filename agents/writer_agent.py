import os


class Agent:
    def __init__(self):
        pass

    def write_comparison(self, summary_a: str, summary_b: str, output_path: str):
        """
        Writes a simple text-based comparison document.
        Even though the extension is .docx, we'll write plain text for now.
        """
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        lines = []
        lines.append("Comparison Report")
        lines.append("")
        lines.append("Document A Summary:")
        lines.append(summary_a)
        lines.append("")
        lines.append("Document B Summary:")
        lines.append(summary_b)

        with open(output_path, "w") as f:
            f.write("\n".join(lines))

        print(f"[WriterAgent] Comparison written to: {output_path}")
