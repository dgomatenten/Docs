"""
Django integration helpers for MD Viewer.

Usage in ``urls.py``::

    from mdviewer.django_ext import get_urlpatterns

    urlpatterns = [
        path("admin/", admin.site.urls),
        *get_urlpatterns("/path/to/docs", prefix="docs"),
    ]
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Optional

from .manager import FileNode, MarkdownManager

try:
    from django.http import HttpRequest, HttpResponse, JsonResponse, Http404
    from django.shortcuts import render as django_render
    from django.urls import path as django_path
    _DJANGO_AVAILABLE = True
except ImportError:
    _DJANGO_AVAILABLE = False


def _require_django():
    if not _DJANGO_AVAILABLE:
        raise ImportError("Django is not installed.  Install it with: pip install django")


def _tree_to_json(nodes: list[FileNode]) -> list[dict]:
    out = []
    for n in nodes:
        out.append({
            "name": n.name,
            "path": n.slug,
            "is_dir": n.is_dir,
            "children": _tree_to_json(n.children) if n.is_dir else [],
        })
    return out


def get_urlpatterns(
    root_dir: str | os.PathLike,
    prefix: str = "docs",
    extra_extensions: Optional[list] = None,
):
    """
    Return a list of Django URL patterns for the Markdown viewer.

    Example::

        urlpatterns += get_urlpatterns("/my/docs", prefix="docs")
        # Viewer at /docs/, /docs/view/<path>
    """
    _require_django()
    root_dir = Path(root_dir).resolve()
    manager = MarkdownManager(root_dir, extra_extensions)
    root_label = root_dir.name

    def _ctx(page, active_path):
        return {
            "tree_json": json.dumps(_tree_to_json(manager.get_tree())),
            "page": page,
            "active_path": active_path,
            "root_label": root_label,
            "blueprint_name": prefix,
        }

    def index_view(request: "HttpRequest") -> "HttpResponse":
        readme = manager.find_readme()
        page, active = None, ""
        if readme:
            try:
                page = manager.render(readme)
                active = readme
            except Exception:
                pass
        return django_render(request, "mdviewer/viewer.html", _ctx(page, active))

    def doc_view(request: "HttpRequest", rel_path: str) -> "HttpResponse":
        try:
            page = manager.render(rel_path)
        except FileNotFoundError:
            raise Http404("Markdown file not found.")
        except PermissionError:
            from django.core.exceptions import PermissionDenied
            raise PermissionDenied()
        return django_render(request, "mdviewer/viewer.html", _ctx(page, rel_path))

    def api_tree(request: "HttpRequest") -> "JsonResponse":
        return JsonResponse(_tree_to_json(manager.get_tree()), safe=False)

    def api_render(request: "HttpRequest", rel_path: str) -> "JsonResponse":
        try:
            return JsonResponse(manager.render(rel_path))
        except FileNotFoundError:
            return JsonResponse({"error": "not found"}, status=404)
        except PermissionError:
            return JsonResponse({"error": "forbidden"}, status=403)

    def api_search(request: "HttpRequest") -> "JsonResponse":
        q = request.GET.get("q", "")
        return JsonResponse(manager.search(q), safe=False)

    return [
        django_path(f"{prefix}/", index_view, name=f"{prefix}_index"),
        django_path(f"{prefix}/view/<path:rel_path>", doc_view, name=f"{prefix}_doc"),
        django_path(f"{prefix}/api/tree", api_tree, name=f"{prefix}_api_tree"),
        django_path(f"{prefix}/api/render/<path:rel_path>", api_render, name=f"{prefix}_api_render"),
        django_path(f"{prefix}/api/search", api_search, name=f"{prefix}_api_search"),
    ]
