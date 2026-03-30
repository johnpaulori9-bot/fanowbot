import os


class Workflow:
    def run(self, agents, **kwargs):
        pdf_agent = agents.get("PdfAgent")
        writer_agent = agents.get("WriterAgent")

        if not pdf_agent:
            raise ValueError("PdfAgent not found.")
        if not writer_agent:
            raise ValueError("WriterAgent not found.")

        file_a = "/mnt/c/Users/admin/Downloads/policy_a.pdf"
        file_b = "/mnt/c/Users/admin/Downloads/policy_b.pdf"
        output_path = "/mnt/c/Users/admin/Downloads/apex_compare_output.docx"

        if not os.path.exists(file_a):
            raise FileNotFoundError(f"File not found: {file_a}")
        if not os.path.exists(file_b):
            raise FileNotFoundError(f"File not found: {file_b}")

        print(f"[CompareWorkflow] Summarizing: {file_a}")
        summary_a = pdf_agent.summarize(file_a)

        print(f"[CompareWorkflow] Summarizing: {file_b}")
        summary_b = pdf_agent.summarize(file_b)

        print("[CompareWorkflow] Writing comparison document...")
        writer_agent.write_comparison(summary_a, summary_b, output_path)

        print(f"[CompareWorkflow] Comparison written to: {output_path}")
        return output_path
