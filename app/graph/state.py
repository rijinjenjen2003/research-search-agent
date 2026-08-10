from typing import TypedDict


class VerificationResult(TypedDict):
    status: str
    confidence: str
    supported_claims: list[str]
    conflicts: list[str]
    uncertainties: list[str]
    recommendation: str


class ResearchState(TypedDict, total=False):

    question: str

    search_queries: list[str]

    search_results: list[dict]

    unique_results: list[dict]

    approved_sources: list[dict]

    rejected_sources: list[dict]

    verification: VerificationResult

    final_answer: str