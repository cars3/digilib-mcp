"""Export — builds the LaTeX source for a DigiLIB research export.

The calling LLM supplies the conversation summary and the recommended-
literature list directly; this module turns them into a complete LaTeX
document (literature review + conversation summary + citations).

It returns the LaTeX SOURCE string and does not compile a PDF, so no TeX
installation is needed on the server side — the caller (or the user)
renders it however they like.
"""

import re

# --------------------------------------------------------------------------
# LaTeX helpers
# --------------------------------------------------------------------------

def _escape(text: str) -> str:
    """Escape special LaTeX characters in plain text."""
    replacements = [
        ("\\", r"\textbackslash{}"),
        ("&", r"\&"), ("%", r"\%"), ("$", r"\$"),
        ("#", r"\#"), ("_", r"\_"), ("{", r"\{"), ("}", r"\}"),
        ("~", r"\textasciitilde{}"), ("^", r"\textasciicircum{}"),
    ]
    for char, escaped in replacements:
        text = text.replace(char, escaped)
    return text


def _build_items(literature_text: str) -> str:
    items = []
    for line in literature_text.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        line = re.sub(r"^[\-\*\d]+[\.\)]\s*", "", line)
        items.append(r"\item " + _escape(line))
    return "\n".join(items)


def _format_citation(article: dict, fmt: str) -> str:
    # Accept both capitalized (Title/Authors/Year/Link) and lowercase keys.
    title   = _escape(article.get("Title", article.get("title", "Untitled")))
    authors = _escape(article.get("Authors", article.get("authors", "Unknown")))
    year    = _escape(str(article.get("Year", article.get("year", "n.d.")) or "n.d."))
    link    = article.get("Link", article.get("link", ""))
    link_tex = rf"\url{{{link}}}" if link else "---"

    if fmt == "APA":
        return rf"{authors} ({year}). {title}. {link_tex}"
    if fmt == "Chicago":
        return rf"{authors}. ``{title}.'' {year}. {link_tex}."
    if fmt == "MLA":
        return rf"{authors}. ``{title}.'' {year}. Web. {link_tex}."
    return rf"{authors} ({year}). {title}. {link_tex}"


def _build_citations_section(liked_articles: list, formats: list) -> str:
    if not liked_articles or not formats:
        return ""
    parts = [r"\section*{Citations}"]
    for fmt in formats:
        items_tex = "\n".join(
            rf"\item {_format_citation(a, fmt)}" for a in liked_articles
        )
        parts.append(
            rf"\subsection*{{{_escape(fmt)} Format}}"
            "\n"
            r"\begin{enumerate}"
            "\n"
            r"\setlength{\itemsep}{6pt}"
            "\n"
            + items_tex
            + "\n"
            + r"\end{enumerate}"
        )
    return "\n\n".join(parts)


# --------------------------------------------------------------------------
# Public entry point
# --------------------------------------------------------------------------

def export_research(
    conversation_summary: str,
    literature_recommended: list,
    liked_articles: list = None,
    citation_formats: list = None,
) -> str:
    """Build the LaTeX source for a research export and return it as a string.

    Args:
        conversation_summary:   plain-text summary of the conversation, supplied
                                by the calling LLM.
        literature_recommended: list of plain-text lines for the Literature
                                Review section (one LaTeX item per line). A
                                single multi-line string is also accepted.
        liked_articles:        list of dicts with Title/Authors/Year/Link keys
                                (or lowercase equivalents) for the citations.
        citation_formats:      subset of ["APA", "Chicago", "MLA"].

    Returns:
        The complete LaTeX document source. Render it with any TeX tool, e.g.
        `pdflatex document.tex`, or hand it to the user as-is.
    """
    # literature_recommended may arrive as a single multi-line string or a list.
    if isinstance(literature_recommended, str):
        literature_recommended = literature_recommended.splitlines()

    lit_items = _build_items("\n".join(literature_recommended))
    summary_escaped = _escape(conversation_summary or "")

    literature_section = rf"""
\section*{{Literature Review}}
\begin{{itemize}}
{lit_items}
\end{{itemize}}
\vspace{{2em}}""" if lit_items.strip() else ""

    citations_section = _build_citations_section(liked_articles or [], citation_formats or [])
    if citations_section:
        citations_section = "\n\\vspace{2em}\n" + citations_section

    latex = rf"""
\documentclass[12pt,a4paper]{{article}}
\usepackage[margin=1in]{{geometry}}
\usepackage{{lmodern}}
\usepackage[T1]{{fontenc}}
\usepackage[utf8]{{inputenc}}
\usepackage{{hyperref}}
\hypersetup{{colorlinks=true,urlcolor=blue,pdfborder={{0 0 0}}}}
\title{{\textbf{{DigiLIB Research Export}}}}
\date{{\today}}
\begin{{document}}
\maketitle
\thispagestyle{{empty}}
\vspace{{1em}}\hrule\vspace{{2em}}
{literature_section}
\section*{{Conversation Summary}}
{summary_escaped}
{citations_section}
\vfill
\hrule
\vspace{{0.5em}}
\begin{{center}}\small Exported from \textbf{{DigiLIB}} research assistant\end{{center}}
\end{{document}}
"""

    return latex.strip()
