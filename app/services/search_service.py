from tavily import TavilyClient

from app.core.config import settings


class SearchService:

    def __init__(self):
        self.client = TavilyClient(
            api_key=settings.tavily_api_key
        )

    def search(
        self,
        query: str,
        max_results: int = 5
    ) -> list[dict]:

        response = self.client.search(
            query=query,
            search_depth="advanced",
            max_results=max_results,
            include_answer=False,
            include_raw_content=False
        )

        results = []

        for result in response.get("results", []):
            results.append({
                "title": result.get("title"),
                "url": result.get("url"),
                "content": result.get("content"),
                "score": result.get("score")
            })

        return results