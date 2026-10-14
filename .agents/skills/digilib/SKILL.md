---
name: digilib
description: >-
  Digital librarian: search academic papers (OpenAlex, arXiv, Semantic
  Scholar, Crossref) and books (Open Library, Google Books) across six free
  sources, and export a cited literature review as LaTeX. Use when the user
  asks to research a topic, find papers or books, check the literature,
  build a reading list, or produce a cited research summary.
license: MIT
---

# digilib — digital librarian

digilib is an MCP server that gives you (the calling agent) the abilities of
a digital librarian: multi-source literature search and LaTeX research
export. DigiLIB stands for "digital librarian". No API keys are required.

## Tools

### search_papers(keywords, year_from?, year_to?, size?) -> str
Searches OpenAlex, arXiv, Semantic Scholar, and Crossref concurrently.
- `keywords`: your search queries — pass 2-5 focused variants per topic.
  Expand acronyms, add synonyms, use technical phrasing (e.g.
  "retrieval-augmented generation" rather than "RAG paper").
- `year_from` / `year_to`: restrict by publication year (applied by OpenAlex
  and Crossref only).
- `size`: results per source per keyword (default 10, max 40).
Returns a numbered plain-text list; the header echoes the queries and shows
per-source hit counts.

### search_books(keywords, size?) -> str
Searches Open Library and Google Books. Broader, book-friendly phrasing
works better here than for papers.

### export_research_tool(conversation_summary, literature_recommended, liked_articles?, citation_formats?) -> str
Builds a complete LaTeX document (literature review + conversation summary +
citations). Write the returned source to a `.tex` file; compile with
`pdflatex` if available, otherwise hand the user the file (Overleaf compiles
it too). Pass `citation_formats` as a subset of ["APA", "Chicago", "MLA"].

## Recommended workflow

1. Understand the actual question; derive 2-5 strong paper queries and 1-3
   book queries.
2. Call `search_papers` and/or `search_books`.
3. Check the per-source hit header; a `source=0` can be transient — a retry
   is cheap.
4. Synthesize for the user; cite only what the tools returned. Never invent
   citations, links, or authors.
5. Offer a durable writeup when it fits: call `export_research_tool`, save
   the LaTeX, compile or hand it over.

## Persona

This server also carries the DigiLIB persona prompt: the `digilib_researcher`
prompt and the `digilib://prompts/researcher` resource. Load it when the
user wants the digital-librarian voice and character; the workflow above
stands on its own otherwise.

## Connecting digilib to an agent

Registration snippets for every supported agent live in `docs/agents/` of
this repository. Canonical instructions: `AGENTS.md`.
