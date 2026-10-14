"""PaperService — academic paper search across four free sources.

Sources: OpenAlex, arXiv, Semantic Scholar, Crossref. All keyless. Each
source method returns the unified schema from services.base; failures are
contained per source.
"""

import asyncio
import re
import xml.etree.ElementTree as ET

import httpx
import requests

from ..config import HTTP_TIMEOUT, OPENALEX_EMAIL
from .base import dedupe_by_title, format_results, normalize_result

ARXIV_NS = {"atom": "http://www.w3.org/2005/Atom"}


class PaperService:
    SOURCE_NAMES = ("openalex", "arxiv", "semantic_scholar", "crossref")

    # ------------------------------------------------------------------ #
    # Individual sources                                                  #
    # ------------------------------------------------------------------ #

    async def _openalex(self, client, keyword, size=10, year_from=None, year_to=None):
        headers = {"User-Agent": f"mailto:{OPENALEX_EMAIL}"} if OPENALEX_EMAIL else {}
        filters = ["has_abstract:true"]
        if year_from:
            filters.append(f"from_publication_date:{year_from}-01-01")
        if year_to:
            filters.append(f"to_publication_date:{year_to}-12-31")

        r = await client.get(
            "https://api.openalex.org/works",
            params={"search": keyword, "per-page": size, "filter": ",".join(filters)},
            headers=headers,
        )
        results = []
        if r.status_code != 200:
            return results

        for w in r.json().get("results", []):
            authors = ", ".join(
                (a.get("author", {}).get("display_name") or "Unknown")
                for a in w.get("authorships", [])
            ) or "Unknown"

            # OpenAlex ships abstracts as an inverted word index — reassemble.
            abstract_data = w.get("abstract_inverted_index")
            if abstract_data:
                sorted_words = sorted(
                    (pos, word)
                    for word, positions in abstract_data.items()
                    for pos in positions
                )
                abstract = " ".join(word for _, word in sorted_words)
            else:
                abstract = "No abstract available."

            doi = w.get("doi")
            link = doi or w.get("id", "")
            results.append(normalize_result(
                title=w.get("display_name", "Untitled"),
                authors=authors,
                year=w.get("publication_year"),
                link=link,
                abstract=abstract,
                source="openalex",
                kind="paper",
                doi=(doi.replace("https://doi.org/", "") if doi else None),
                citations=w.get("cited_by_count"),
            ))
        return results

    async def _arxiv(self, client, keyword, size=10):
        # arXiv's edge WAF blocks httpx's fingerprint (406) but accepts the
        # `requests` library, so route through it in a worker thread.
        def _fetch():
            return requests.get(
                "https://export.arxiv.org/api/query",
                params={
                    "search_query": f"all:{keyword}",
                    "max_results": size,
                    "sortBy": "relevance",
                },
                timeout=HTTP_TIMEOUT,
                headers={"User-Agent": f"mailto:{OPENALEX_EMAIL}"} if OPENALEX_EMAIL else {},
            )

        r = await asyncio.to_thread(_fetch)
        results = []
        if r.status_code != 200:
            return results

        root = ET.fromstring(r.text)
        for entry in root.findall("atom:entry", ARXIV_NS):
            title = (entry.findtext("atom:title", default="", namespaces=ARXIV_NS) or "").strip()
            abstract = (entry.findtext("atom:summary", default="", namespaces=ARXIV_NS) or "").strip()
            link = (entry.findtext("atom:id", default="", namespaces=ARXIV_NS) or "").strip()
            published = entry.findtext("atom:published", default="", namespaces=ARXIV_NS) or ""
            year = published[:4] or None
            authors = [a.findtext("atom:name", default="", namespaces=ARXIV_NS)
                       for a in entry.findall("atom:author", ARXIV_NS)]
            results.append(normalize_result(
                title=title, authors=authors, year=year, link=link,
                abstract=abstract, source="arxiv", kind="preprint",
            ))
        return results

    async def _semantic_scholar(self, client, keyword, size=10):
        # Unauthenticated Semantic Scholar is rate-limited; one retry with a
        # short backoff helps, and any failure is contained (other sources run).
        for attempt in range(2):
            r = await client.get(
                "https://api.semanticscholar.org/graph/v1/paper/search",
                params={
                    "query": keyword,
                    "limit": size,
                    "fields": "title,authors,year,abstract,url,citationCount,externalIds",
                },
            )
            if r.status_code != 429:
                break
            await asyncio.sleep(1.5 * (attempt + 1))
        results = []
        if r.status_code != 200:
            return results

        for p in r.json().get("data", []):
            if not p.get("title"):
                continue
            authors = ", ".join(a.get("name", "Unknown") for a in p.get("authors") or []) or "Unknown"
            doi = (p.get("externalIds") or {}).get("DOI")
            results.append(normalize_result(
                title=p["title"], authors=authors, year=p.get("year"),
                link=p.get("url") or "", abstract=p.get("abstract") or "No abstract available.",
                source="semantic_scholar", kind="paper", doi=doi,
                citations=p.get("citationCount"),
            ))
        return results

    async def _crossref(self, client, keyword, size=10, year_from=None, year_to=None):
        filters = {"type": "journal-article"}
        if year_from:
            filters["from-pub-date"] = f"{year_from}-01-01"
        if year_to:
            filters["until-pub-date"] = f"{year_to}-12-31"

        r = await client.get(
            "https://api.crossref.org/works",
            params={"query": keyword, "rows": size, "select":
                    "title,author,issued,abstract,URL,DOI,is-referenced-by-count",
                    "filter": ",".join(f"{k}:{v}" for k, v in filters.items())},
        )
        results = []
        if r.status_code != 200:
            return results

        for w in r.json().get("message", {}).get("items", []):
            title_list = w.get("title") or ["Untitled"]
            authors = ", ".join(
                f"{a.get('given', '')} {a.get('family', '')}".strip()
                for a in w.get("author") or []
            ) or "Unknown"
            issued = w.get("issued", {}).get("date-parts", [[None]])[0][0]
            # Crossref abstracts are JATS XML — strip the tags.
            abstract = re.sub(r"<[^>]+>", " ", w.get("abstract") or "").strip() or "No abstract available."
            abstract = re.sub(r"\s+", " ", abstract)
            results.append(normalize_result(
                title=title_list[0], authors=authors, year=issued,
                link=w.get("URL", ""), abstract=abstract,
                source="crossref", kind="paper", doi=w.get("DOI"),
                citations=w.get("is-referenced-by-count"),
            ))
        return results

    # ------------------------------------------------------------------ #
    # Orchestration                                                       #
    # ------------------------------------------------------------------ #

    async def _search_one_keyword(self, client, keyword, size, year_from, year_to):
        """Fan out to every source for one keyword, tolerating per-source failure."""
        tasks = [
            self._openalex(client, keyword, size, year_from, year_to),
            self._arxiv(client, keyword, size),
            self._semantic_scholar(client, keyword, size),
            self._crossref(client, keyword, size, year_from, year_to),
        ]
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        flat, counts = [], dict.fromkeys(self.SOURCE_NAMES, 0)
        for name, resp in zip(self.SOURCE_NAMES, responses):
            if isinstance(resp, Exception):
                continue
            flat.extend(resp)
            counts[name] = len(resp)
        return flat, counts

    async def search(self, keywords, size=10, year_from=None, year_to=None) -> str:
        """Search all keywords across all sources concurrently, dedupe, format."""
        async with httpx.AsyncClient(timeout=HTTP_TIMEOUT, follow_redirects=True) as client:
            tasks = [
                self._search_one_keyword(client, kw, size, year_from, year_to)
                for kw in keywords
            ]
            all_outcomes = await asyncio.gather(*tasks)

        flat, totals = [], dict.fromkeys(self.SOURCE_NAMES, 0)
        for results, counts in all_outcomes:
            flat.extend(results)
            for name, count in counts.items():
                totals[name] += count

        combined = dedupe_by_title(flat)
        header = (
            f"Paper search results for: {', '.join(keywords)}"
            f" (per-source hits: {', '.join(f'{k}={v}' for k, v in totals.items())})"
        )
        return format_results(combined, header)
