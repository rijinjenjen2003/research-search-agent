from urllib.parse import urlparse, urlunparse


class DeduplicationService:

    @staticmethod
    def normalize_url(url: str) -> str:
        """
        Normalize a URL so tracking parameters and
        minor URL differences do not create duplicates.
        """

        parsed = urlparse(url)

        # Remove query parameters and fragments
        normalized = urlunparse(
            (
                parsed.scheme,
                parsed.netloc.lower(),
                parsed.path.rstrip("/"),
                "",
                "",
                ""
            )
        )

        return normalized

    def remove_duplicates(self, results: list[dict]) -> list[dict]:

        unique_results = []
        seen_urls = set()

        for result in results:

            url = result.get("url")

            if not url:
                continue

            normalized_url = self.normalize_url(url)

            if normalized_url in seen_urls:
                continue

            seen_urls.add(normalized_url)

            result["url"] = normalized_url

            unique_results.append(result)

        return unique_results