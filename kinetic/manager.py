"""
Core logic for the Kinetic Markdown Viewer.
Handles directory scanning and Markdown rendering.
"""
from __future__ import annotations

import os
import pathlib
import re
from dataclasses import dataclass, field
from typing import Optional

import markdown
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.toc import TocExtension


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class FileNode:
    """Represents a file or directory in the doc tree."""
    name: str
    path: str            # relative path from the root
    abs_path: str        # absolute fs path
    is_dir: bool
    children: list["FileNode"] = field(default_factory=list)

    @property
    def slug(self) -> str:
        """URL-safe version of the relative path."""
        return self.path.replace(os.sep, "/")


# ---------------------------------------------------------------------------
# Manager
# ---------------------------------------------------------------------------

class MarkdownManager:
    """
    The central object of the library.

    Parameters
    ----------
    root_dir : str | os.PathLike
        Directory whose Markdown files should be served.
    extensions : list[str] | None
        Extra python-markdown extensions to enable on top of the defaults.
    """

    _DEFAULT_EXTENSIONS = [
        "markdown.extensions.tables",
        "markdown.extensions.fenced_code",
        "markdown.extensions.attr_list",
        "markdown.extensions.def_list",
        "markdown.extensions.admonition",
        "markdown.extensions.footnotes",
        "markdown.extensions.meta",
        "markdown.extensions.nl2br",
        "markdown.extensions.sane_lists",
        "markdown.extensions.smarty",
        "markdown.extensions.abbr",
        "markdown.extensions.md_in_html",
        "pymdownx.superfences",
        "pymdownx.highlight",
        "pymdownx.inlinehilite",
        "pymdownx.tasklist",
        "pymdownx.tilde",
        "pymdownx.emoji",
        "pymdownx.details",
        "pymdownx.critic",
        "pymdownx.magiclink",
        TocExtension(permalink=True, slugify=_slugify),
        CodeHiliteExtension(linenums=False, css_class="highlight"),
    ]

    def __init__(
        self,
        root_dir: str | os.PathLike,
        extra_extensions: Optional[list] = None,
    ):
        self.root = pathlib.Path(root_dir).resolve()
        if not self.root.is_dir():
            raise ValueError(f"root_dir must be an existing directory: {self.root}")
        self._extensions = list(self._DEFAULT_EXTENSIONS) + (extra_extensions or [])

    # ------------------------------------------------------------------
    # Directory tree
    # ------------------------------------------------------------------

    def get_tree(self) -> list[FileNode]:
        """Return the sorted file node tree rooted at *root*."""
        return _build_tree(self.root, self.root)

    # ------------------------------------------------------------------
    # Rendering
    # ------------------------------------------------------------------

    def render(self, rel_path: str) -> dict:
        """
        Render a Markdown file located at *rel_path* (relative to root).

        Returns a dict with keys:
            - ``html``        : rendered HTML string
            - ``toc``         : table-of-contents HTML
            - ``title``       : inferred page title
            - ``rel_path``    : the path that was rendered
        """
        # Sanitise: prevent path traversal
        target = (self.root / rel_path).resolve()
        if not str(target).startswith(str(self.root)):
            raise PermissionError("Path traversal detected.")
        if not target.is_file() or target.suffix.lower() not in {".md", ".markdown"}:
            raise FileNotFoundError(f"Markdown file not found: {rel_path}")

        source = target.read_text(encoding="utf-8")

        md = markdown.Markdown(extensions=self._extensions)
        html = md.convert(source)
        toc = getattr(md, "toc", "")
        title = _extract_title(source) or target.stem.replace("_", " ").replace("-", " ").title()

        return {
            "html": html,
            "toc": toc,
            "title": title,
            "rel_path": rel_path,
        }

    def find_readme(self) -> Optional[str]:
        """Return the relative path of a README file at root level, or None."""
        for name in ("README.md", "readme.md", "index.md", "INDEX.md"):
            if (self.root / name).is_file():
                return name
        return None

    def search(self, query: str) -> list[dict]:
        """
        Simple full-text search across all Markdown files.
        Returns list of dicts with ``rel_path``, ``title``, and ``snippet``.
        """
        query_lower = query.strip().lower()
        if not query_lower:
            return []
        results = []
        for md_file in self.root.rglob("*.md"):
            try:
                text = md_file.read_text(encoding="utf-8")
            except OSError:
                continue
            if query_lower in text.lower():
                rel = str(md_file.relative_to(self.root))
                idx = text.lower().find(query_lower)
                start = max(0, idx - 60)
                snippet = "…" + text[start : idx + 120].replace("\n", " ") + "…"
                results.append({
                    "rel_path": rel,
                    "title": _extract_title(text) or md_file.stem,
                    "snippet": snippet,
                })
        return results


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _build_tree(directory: pathlib.Path, root: pathlib.Path) -> list[FileNode]:
    nodes: list[FileNode] = []
    try:
        entries = sorted(directory.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower()))
    except PermissionError:
        return nodes

    for entry in entries:
        if entry.name.startswith("."):
            continue
        rel = str(entry.relative_to(root))
        if entry.is_dir():
            children = _build_tree(entry, root)
            if children:  # only include dirs that contain md files
                nodes.append(FileNode(
                    name=entry.name,
                    path=rel,
                    abs_path=str(entry),
                    is_dir=True,
                    children=children,
                ))
        elif entry.suffix.lower() in {".md", ".markdown"}:
            nodes.append(FileNode(
                name=entry.name,
                path=rel,
                abs_path=str(entry),
                is_dir=False,
            ))
    return nodes


def _extract_title(text: str) -> Optional[str]:
    """Extract first H1 heading text from Markdown source."""
    m = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
    return m.group(1).strip() if m else None


def _slugify(value: str, separator: str) -> str:
    """A simple ASCII-safe slug function for TOC anchors."""
    value = re.sub(r"[^\w\s-]", "", value).strip().lower()
    return re.sub(r"[\s_-]+", separator, value)
