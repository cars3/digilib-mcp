"""Shared result schema, deduplication, and formatting for DigiLIB services.

Every source (OpenAlex, arXiv, Semantic Scholar, Crossref, Open Library,
Google Books) normalizes its records into the schema below:

    {title, authors, year, link, abstract, source, type, doi?, citations?}
"""

from typing import Optional


def normalize_result(
    title: str,
    authors,
    year,
    link: str,
    abstract: str,
    source: str,
    kind: str,
    doi: Optional[str] = None,
    citations: Optional[int] = None,
) -> dict:
    """Build one unified result record from raw source fields."""
    return {
        "title": (title or "Untitled").strip() or "Untitled",
        "authors": authors.strip() if isinstance(authors, str) else ", ".join(
            a for a in authors if a
        ) or "Unknown",
        "year": year if year not in (None, "") else "n/a",
        "link": link or "",
        "abstract": (abstract or "No abstract available.").strip(),
        "source": source,
        "type": kind,
        "doi": doi,
        "citations": citations,
    }


def dedupe_by_title(results: list) -> list:
    """First occurrence wins, matching on the lower-cased title."""
    seen = set()
    combined = []
    for result in results:
        title = result["title"].lower().strip()
        if title not in seen:
            seen.add(title)
            combined.append(result)
    return combined


def format_results(results: list, header: str) -> str:
    """Numbered plain-text list with a source line per entry, so the calling
    LLM knows where each item came from."""
    if not results:
        return header + "\nNo results found."

    output = [header]
    for i, r in enumerate(results, 1):
        line = (
            f"{i}. {r['title']}\n"
            f"   Authors: {r['authors']}\n"
            f"   Year: {r['year']}\n"
            f"   Type: {r['type']} | Source: {r['source']}"
        )
        if r.get("doi"):
            line += f" | DOI: {r['doi']}"
        if r.get("citations") is not None:
            line += f" | Citations: {r['citations']}"
        line += f"\n   Link: {r['link']}\n   Abstract: {r['abstract'][:300]}"
        output.append(line)
    return "\n".join(output)


def _source_status(sources: dict) -> str:
    """Summarize per-source outcome so a dead source is visible but harmless."""
    parts = []
    for name, count in sources.items():
        parts.append(f"{name}={count}")
    return " | ".join(parts)
