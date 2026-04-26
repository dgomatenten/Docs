"""
Flask extension for the Kinetic Markdown Viewer.

Usage::

    from kinetic.flask_ext import create_blueprint

    bp = create_blueprint("/path/to/docs", url_prefix="/docs")
    app.register_blueprint(bp)

Or using the convenience wrapper::

    from kinetic.flask_ext import md_viewer_blueprint
    app.register_blueprint(md_viewer_blueprint("/path/to/docs"), url_prefix="/docs")
"""
from __future__ import annotations

import json
import os
from pathlib import Path

from flask import (
    Blueprint,
    Response,
    abort,
    current_app,
    jsonify,
    render_template,
    request,
    send_from_directory,
)

from .manager import FileNode, MarkdownManager


def create_blueprint(
    root_dir: str | os.PathLike,
    url_prefix: str = "",
    blueprint_name: str = "kinetic",
    extra_extensions: list | None = None,
) -> Blueprint:
    """
    Build and return a Flask Blueprint that serves Markdown files.

    Parameters
    ----------
    root_dir : str | Path
        Root directory containing Markdown files.
    url_prefix : str
        URL prefix to mount the blueprint on (set when registering,
        or pass it here for self-contained use).
    blueprint_name : str
        Internal Flask blueprint name (must be unique per app).
    extra_extensions : list | None
        Additional python-markdown extensions.
    """
    root_dir = Path(root_dir).resolve()
    manager = MarkdownManager(root_dir, extra_extensions)

    # We need this module's templates and static files
    pkg_dir = Path(__file__).parent
    bp = Blueprint(
        blueprint_name,
        __name__,
        template_folder=str(pkg_dir / "templates"),
        static_folder=str(pkg_dir / "static"),
        static_url_path=f"/{blueprint_name}/static",
        url_prefix=url_prefix,
    )

    # ------------------------------------------------------------------ helpers
    def _tree_to_json(nodes: list[FileNode]) -> list[dict]:
        out = []
        for n in nodes:
            d = {
                "name": n.name,
                "path": n.slug,
                "is_dir": n.is_dir,
                "children": _tree_to_json(n.children) if n.is_dir else [],
            }
            out.append(d)
        return out

    # --------------------------------------------------------------------- routes
    @bp.route("/")
    def index():
        readme = manager.find_readme()
        if readme:
            try:
                page = manager.render(readme)
                tree = _tree_to_json(manager.get_tree())
                return render_template(
                    "kinetic/viewer.html",
                    tree_json=json.dumps(tree),
                    page=page,
                    active_path=readme,
                    root_label=root_dir.name,
                    blueprint_name=blueprint_name,
                )
            except Exception:
                pass

        tree = _tree_to_json(manager.get_tree())
        return render_template(
            "kinetic/viewer.html",
            tree_json=json.dumps(tree),
            page=None,
            active_path="",
            root_label=root_dir.name,
            blueprint_name=blueprint_name,
        )

    @bp.route("/view/<path:rel_path>")
    def view(rel_path: str):
        try:
            page = manager.render(rel_path)
        except FileNotFoundError:
            abort(404)
        except PermissionError:
            abort(403)
        tree = _tree_to_json(manager.get_tree())
        return render_template(
            "kinetic/viewer.html",
            tree_json=json.dumps(tree),
            page=page,
            active_path=rel_path,
            root_label=root_dir.name,
            blueprint_name=blueprint_name,
        )

    @bp.route("/api/tree")
    def api_tree():
        return jsonify(_tree_to_json(manager.get_tree()))

    @bp.route("/api/render/<path:rel_path>")
    def api_render(rel_path: str):
        try:
            return jsonify(manager.render(rel_path))
        except FileNotFoundError:
            return jsonify({"error": "not found"}), 404
        except PermissionError:
            return jsonify({"error": "forbidden"}), 403

    @bp.route("/api/search")
    def api_search():
        q = request.args.get("q", "")
        return jsonify(manager.search(q))

    return bp


# Convenience alias
md_viewer_blueprint = create_blueprint
