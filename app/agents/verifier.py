import json

from langchain_groq import ChatGroq

from app.core.config import settings


class VerificationAgent:

    def __init__(self):

        self.llm = ChatGroq(
            model=settings.llm_model,
            api_key=settings.groq_api_key,
            temperature=0
        )

    def verify(
        self,
        question: str,
        sources: list[dict]
    ) -> dict:

        sources = sources[:8]

        evidence_text = ""

        for index, source in enumerate(
            sources,
            start=1
        ):

            content = source.get(
                "content",
                ""
            )[:1200]

            evidence_text += f"""
SOURCE {index}

Title:
{source.get("title")}

URL:
{source.get("url")}

Content:
{content}

-------------------------
"""

        prompt = f"""
You are an evidence verification agent.

Research question:
{question}

Evidence collected from multiple sources:

{evidence_text}

Analyze the evidence.

Return ONLY valid JSON.

Use exactly this structure:

{{
    "status": "SUPPORTED",
    "confidence": "HIGH",
    "supported_claims": [
        "claim supported by the evidence"
    ],
    "conflicts": [],
    "uncertainties": [],
    "recommendation": "No additional research required"
}}

Allowed status values:

SUPPORTED
CONFLICTING
INSUFFICIENT

Allowed confidence values:

HIGH
MEDIUM
LOW

Rules:

- SUPPORTED means the evidence is sufficient.
- CONFLICTING means important sources disagree.
- INSUFFICIENT means there is not enough evidence.
- Do not invent claims.
- Put unresolved information in uncertainties.
- If there are no conflicts, return an empty conflicts list.
- If there are no uncertainties, return an empty uncertainties list.
"""

        response = self.llm.invoke(prompt)

        content = response.content.strip()

        # Remove markdown code fences if the model adds them
        if content.startswith("```"):
            content = content.replace(
                "```json",
                ""
            ).replace(
                "```",
                ""
            ).strip()

        try:

            verification = json.loads(content)

        except json.JSONDecodeError:

            return {
                "status": "INSUFFICIENT",
                "confidence": "LOW",
                "supported_claims": [],
                "conflicts": [],
                "uncertainties": [
                    "Verifier returned invalid structured output."
                ],
                "recommendation": "Perform additional research."
            }

        return verification