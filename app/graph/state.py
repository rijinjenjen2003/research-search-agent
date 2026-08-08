from typing import TypedDict


class ResearchState(TypedDict, total=False):

    question: str

    search_queries: list[str]

    search_results: list[dict]

    unique_results: list[dict]

    verification: dict

    final_answer: str