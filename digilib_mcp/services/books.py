"""BookService — book search across Open Library and Google Books.

Both sources are keyless. Results normalize to the same unified schema as
papers, with `type: "book"`.
"""

import asyncio

import httpx

from ..config import GOOGLE_BOOKS_API_KEY, HTTP_TIMEOUT
from .base import dedupe_by_title, format_results, normalize_result


class BookService:
    SOURCE_NAMES = ("open_library", "google_books")

    # ------------------------------------------------------------------ #
    # Individual sources                                                  #
    # ------------------------------------------------------------------ #

    async def _open_library(self, client, keyword, size=10):
        r = await client.get(
            "https://openlibrary.org/search.json",
            params={
                "q": keyword,
                "limit": size,
                "fields": "title,author_name,first_publish_year,key,first_sentence,subject",
            },
        )
        results = []
        if r.status_code != 200:
            return results

        for b in r.json().get("docs", []):
            # Prefer the first sentence of the book, fall back to subject tags.
            first_sentence = b.get("first_sentence")
            # Open Library returns a list of plain strings (older responses used
            # a list of {"text": ...} dicts), so accept either shape.
            if isinstance(first_sentence, list):
                first = first_sentence[0] if first_sentence else ""
                first_sentence = first.get("text", "") if isinstance(first, dict) else str(first)
            abstract = first_sentence or (
                "Subjects: " + ", ".join(b.get("subject", [])[:8])
                if b.get("subject") else "No abstract available."
            )
            results.append(normalize_result(
                title=b.get("title", "Untitled"),
                authors=b.get("author_name") or ["Unknown"],
                year=b.get("first_publish_year"),
                link="https://openlibrary.org" + b.get("key", ""),
                abstract=abstract,
                source="open_library",
                kind="book",
            ))
        return results

    async def _google_books(self, client, keyword, size=10):
        params = {"q": keyword, "maxResults": size}
        # Optional key for reliable quota; no-key search works but is rate-limited.
        if GOOGLE_BOOKS_API_KEY:
            params["key"] = GOOGLE_BOOKS_API_KEY
        r = await client.get(
            "https://www.googleapis.com/books/v1/volumes",
            params=params,
        )
        results = []
        if r.status_code != 200:
            return results

        for item in r.json().get("items", []):
            info = item.get("volumeInfo", {})
            published = info.get("publishedDate") or ""
            results.append(normalize_result(
                title=info.get("title", "Untitled"),
                authors=info.get("authors") or ["Unknown"],
                year=published[:4],
                link=info.get("canonicalVolumeLink") or info.get("infoLink") or "",
                abstract=info.get("description") or "No abstract available.",
                source="google_books",
                kind="book",
            ))
        return results

    # ------------------------------------------------------------------ #
    # Orchestration                                                       #
    # ------------------------------------------------------------------ #

    async def search(self, keywords, size=10) -> str:
        """Search all keywords across both book sources concurrently, dedupe, format."""
        async with httpx.AsyncClient(timeout=HTTP_TIMEOUT, follow_redirects=True) as client:
            tasks = []
            for kw in keywords:
                tasks.append(self._open_library(client, kw, size))
                tasks.append(self._google_books(client, kw, size))
            responses = await asyncio.gather(*tasks, return_exceptions=True)

        flat, totals = [], dict.fromkeys(self.SOURCE_NAMES, 0)
        for name, resp in zip([n for _ in keywords for n in self.SOURCE_NAMES], responses):
            if isinstance(resp, Exception):
                continue
            flat.extend(resp)
            totals[name] += len(resp)

        combined = dedupe_by_title(flat)
        header = (
            f"Book search results for: {', '.join(keywords)}"
            f" (per-source hits: {', '.join(f'{k}={v}' for k, v in totals.items())})"
        )
        return format_results(combined, header)