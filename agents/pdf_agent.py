from PyPDF2 import PdfReader


class Agent:
    def __init__(self, llm=None):
        self.llm = llm

    def _extract_text(self, file_path: str) -> str:
        reader = PdfReader(file_path)
        chunks = []
        for page in reader.pages:
            text = page.extract_text() or ""
            chunks.append(text)
        return "\n".join(chunks)

    def summarize(self, file_path: str) -> str:
        """
        Basic PDF summarization:
        - Extracts text from all pages
        - Truncates to a reasonable length
        - (Later: send to LLM for real summarization)
        """
        print(f"[PdfAgent] Extracting text from: {file_path}")
        full_text = self._extract_text(file_path)

        if not full_text.strip():
            return f"No readable text found in {file_path}."

        # Truncate for now to avoid huge strings
        max_chars = 4000
        truncated = full_text[:max_chars]

        # If you wire an LLM later, you can replace this with a real summary
        print(f"[PdfAgent] Returning truncated text (~{len(truncated)} chars).")
        return truncated
