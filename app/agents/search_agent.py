from app.services.search_service import SearchService


class SearchAgent:

    def __init__(self):
        self.search_service = SearchService()

    def search_queries(
        self,
        queries: list[str]
    ) -> list[dict]:

        all_results = []

        for query in queries:

            results = self.search_service.search(
                query=query,
                max_results=5
            )

            for result in results:
                all_results.append({
                    "query": query,
                    **result
                })

        return all_results