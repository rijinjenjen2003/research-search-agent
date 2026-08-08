from langchain_groq import ChatGroq

from app.core.config import settings


class SynthesizerAgent:

    def __init__(self):
        self.llm = ChatGroq(
            model=settings.llm_model,
            api_key=settings.groq_api_key,
            temperature=0
        )

    def synthesize(
        self,
        question: str,
        sources: list[dict],
        verification: dict
    ) -> str:

        evidence_text = ""

        # Limit evidence to avoid Groq token-limit problems
        for index, source in enumerate(sources[:8], start=1):

            content = source.get("content", "")[:1200]

            evidence_text += f"""
SOURCE {index}
Title: {source.get("title")}
URL: {source.get("url")}
Evidence:
{content}

-------------------------
"""

        prompt = f"""
You are a research synthesis agent.

Answer the user's research question using ONLY the
evidence provided below.

Research question:
{question}

Verification analysis:
{verification.get("verification", "")}

Sources:
{evidence_text}

Requirements:

1. Give a clear and factual answer.
2. Do not invent information.
3. Cite claims using [1], [2], etc.
4. Clearly mention conflicting information.
5. Clearly mention uncertainty when evidence is insufficient.
6. Prefer information supported by multiple sources.

Format:

## Answer

Your answer here.

## Uncertainty

Mention uncertainty or write "No major uncertainty identified."

## Sources

[1] Source title - URL
[2] Source title - URL
"""

        response = self.llm.invoke(prompt)

        return response.content