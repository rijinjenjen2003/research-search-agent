from langchain_groq import ChatGroq

from app.core.config import settings
from app.models.schemas import ResearchPlan


class PlannerAgent:

    def __init__(self):
        self.llm = ChatGroq(
            model=  settings.llm_model,
            api_key=settings.groq_api_key,
            temperature=0
        )

        self.structured_llm = self.llm.with_structured_output(
            ResearchPlan
        )

    def create_plan(self, question: str) -> ResearchPlan:

        prompt = f"""
You are a research planning agent.

Your task is to create a reliable search strategy for the
user's research question.

Generate 3 to 5 diverse search queries.

The queries should:
- Cover different aspects of the question
- Prefer specific and factual searches
- Include recent information when relevant
- Help retrieve information from multiple independent sources
- Avoid duplicate or nearly identical queries

User question:
{question}
"""

        return self.structured_llm.invoke(prompt)