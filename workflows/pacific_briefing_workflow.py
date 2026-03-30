import os
from datetime import datetime


class Workflow:
    def run(self, agents, **kwargs):
        web_agent = agents.get("WebAgent")
        pdf_agent = agents.get("PdfAgent")
        writer = agents.get("WriterAgent")
        memory = agents.get("MemoryAgent")

        goal = "Prepare a Pacific/Chuuk-focused briefing for John."
        if memory:
            memory.remember("last_pacific_briefing_goal", goal)

        lines = []
        lines.append("Pacific / Chuuk Briefing")
        lines.append(f"Generated at: {datetime.utcnow().isoformat()} UTC")
        lines.append("")

        # PacificMap / regional context (placeholder)
        if web_agent:
            try:
                web_agent.fetch_text("https://map.pacificdata.org")
                lines.append("- Context: fetched data from PacificMap (details not parsed).")
            except Exception as e:
                lines.append(f"- Context: error fetching PacificMap ({e})")
        else:
            lines.append("- Context: WebAgent not available for PacificMap.")

        # Placeholder for policy PDFs (you can point these to real files later)
        policy_a = "/mnt/c/Users/admin/Downloads/pacific_policy_a.pdf"
        policy_b = "/mnt/c/Users/admin/Downloads/pacific_policy_b.pdf"

        if pdf_agent and os.path.exists(policy_a) and os.path.exists(policy_b):
            lines.append("")
            lines.append("Policy comparison (Pacific):")
            summary_a = pdf_agent.summarize(policy_a)
            summary_b = pdf_agent.summarize(policy_b)
            lines.append(f"- Policy A summary (truncated): {summary_a[:500]}")
            lines.append(f"- Policy B summary (truncated): {summary_b[:500]}")
        else:
            lines.append("")
            lines.append("Policy comparison (Pacific):")
            lines.append("- No policy PDFs found at the expected paths, or PdfAgent unavailable.")

        output_path = "/mnt/c/Users/admin/Downloads/pacific_briefing.txt"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w") as f:
            f.write("\n".join(lines))

        print(f"[PacificBriefingWorkflow] Pacific briefing written to: {output_path}")
        return output_path
