from urllib.parse import urlparse


class SourceFilter:

    # Trusted domains for research
    APPROVED_DOMAINS = {
        "reuters.com",
        "bbc.com",
        "bbc.co.uk",
        "apnews.com",
        "nytimes.com",
        "nature.com",
        "science.org",
        "who.int",
        "gov",
        "edu",
        "arxiv.org",
        "nasa.gov",
        "nih.gov",
        "openai.com",
        "google.com",
        "microsoft.com",
        "ibm.com",
    }

    def is_approved_domain(self, url: str) -> bool:

        try:
            hostname = urlparse(url).netloc.lower()

            # Remove www.
            hostname = hostname.replace("www.", "")

            for domain in self.APPROVED_DOMAINS:

                if (
                    hostname == domain
                    or hostname.endswith("." + domain)
                ):
                    return True

            return False

        except Exception:
            return False

    def filter_sources(
        self,
        sources: list[dict]
    ) -> dict:

        approved = []
        rejected = []

        for source in sources:

            url = source.get("url", "")
            content = source.get("content", "")

            if not url:
                rejected.append({
                    "source": source,
                    "reason": "Missing URL"
                })
                continue

            if not content:
                rejected.append({
                    "source": source,
                    "reason": "Missing content"
                })
                continue

            if not self.is_approved_domain(url):

                rejected.append({
                    "source": source,
                    "reason": "Domain not approved"
                })

                continue

            approved.append(source)

        return {
            "approved": approved,
            "rejected": rejected
        }