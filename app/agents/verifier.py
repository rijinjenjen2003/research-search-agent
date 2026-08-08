from langchain_groq import ChatGroq

from app.core.config import settings


class VerificationAgent:

    def __init__(self):
        self.llm = ChatGroq(
            model=settings.llm_model,
            api_key=settings.groq_api_key,
            temperature=0
        )

    def verify(self, question: str, sources: list[dict]) -> dict:
        sources = sources[:8]

        evidence_text = ""

        for index, source in enumerate(sources, start=1):
            evidence_text += f"""
SOURCE {index}
Title: {source.get("title")}
URL: {source.get("url")}
Content:
{source.get("content", "")}

-------------------------
"""

        prompt = f"""
You are an evidence verification agent.

Research question:
{question}

Below are search results collected from multiple independent sources:

{evidence_text}

Analyze the evidence and determine:

1. What major claims are supported?
2. Whether the sources agree with each other.
3. Whether there are conflicting claims.
4. Whether the evidence is sufficient to answer the question.
5. What information remains uncertain.

Return your analysis using exactly this structure:

STATUS:
SUPPORTED, CONFLICTING, or INSUFFICIENT

CONFIDENCE:
HIGH, MEDIUM, or LOW

SUPPORTED_CLAIMS:
- claim 1
- claim 2

CONFLICTS:
- conflict 1
- NONE if there are no conflicts

UNCERTAINTIES:
- uncertainty 1
- NONE if there are no uncertainties

RECOMMENDATION:
A short recommendation about whether more research is required.
"""

        response = self.llm.invoke(prompt)

        return {
            "verification": response.content
        }