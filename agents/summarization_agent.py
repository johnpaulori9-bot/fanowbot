import re
from typing import List


class Agent:
    """
    SummarizationAgent

    Naive extractive summarizer:
    - Splits text into sentences
    - Scores sentences
    - Returns top N as summary
    """

    def __init__(self, max_sentences: int = 8):
        self.max_sentences = max_sentences

    def _split_sentences(self, text: str) -> List[str]:
        text = text.replace("\n", " ")
        sentences = re.split(r"(?<=[.!?])\s+", text)
        return [s.strip() for s in sentences if s.strip()]

    def summarize(self, text: str, max_sentences: int = None) -> str:
        if not text:
            return ""

        max_sents = max_sentences or self.max_sentences
        sentences = self._split_sentences(text)

        if len(sentences) <= max_sents:
            return " ".join(sentences)

        scored = []
        for idx, s in enumerate(sentences):
            length = len(s.split())
            if length < 5:
                score = 0
            else:
                score = 1.0
                score += max(0.0, 1.0 - (idx / max(1, len(sentences))))
                if length > 40:
                    score -= 0.5
            scored.append((score, idx, s))

        scored.sort(key=lambda x: (-x[0], x[1]))
        top = sorted(scored[:max_sents], key=lambda x: x[1])
        return " ".join([s for _, _, s in top])
