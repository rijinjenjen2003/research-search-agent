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
        source_map = []

        for index, source in enumerate(
            sources[:8],
            start=1
        ):

            title = source.get("title", "Unknown source")
            url = source.get("url", "")
            content = source.get("content", "")[:1200]

            evidence_text += f"""
SOURCE [{index}]

Title:
{title}

URL:
{url}

Evidence:
{content}

-------------------------
"""

            source_map.append({
                "id": index,
                "title": title,
                "url": url
            })

        verification_text = f"""
Status: {verification.get("status")}
Confidence: {verification.get("confidence")}

Supported Claims:
{verification.get("supported_claims")}

Conflicts:
{verification.get("conflicts")}

Uncertainties:
{verification.get("uncertainties")}

Recommendation:
{verification.get("recommendation")}
"""

        prompt = f"""
You are a research synthesis agent.

Answer the user's question using ONLY the provided
approved sources.

Research question:
{question}

Verification:
{verification_text}

Approved sources:

{evidence_text}

Citation rules:

1. Every important factual claim must have a citation.
2. Use the exact source number provided above.
3. Use citations such as [1], [2], [3].
4. Do not create citation numbers that do not exist.
5. A citation must directly support the claim.
6. If multiple sources support a claim, cite multiple sources.
7. Do not use information outside the provided sources.

Requirements:

- Give a clear answer.
- Do not invent information.
- Mention important conflicts.
- Mention uncertainty when evidence is limited.
- Use only approved sources.

Format:

## Answer

Write the answer with citations.

## Confidence

State the confidence level and explain briefly why.

## Uncertainty

Explain important uncertainties.
If there are none, write:
"No major uncertainty identified."

## Sources

[1] Source title - URL
[2] Source title - URL
...
"""

        response = self.llm.invoke(prompt)

        return response.content