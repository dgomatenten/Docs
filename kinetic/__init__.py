"""
Kinetic MD Viewer
=================
A premium Markdown viewer that works as a standalone app
and as a library for Flask / Django.

Quick start (standalone)::

    from kinetic import create_app
    app = create_app("/path/to/docs")
    app.run()

Flask Blueprint::

    from kinetic.flask_ext import md_viewer_blueprint
    app.register_blueprint(md_viewer_blueprint("/path/to/docs"), url_prefix="/docs")

Django::

    # urls.py
    from kinetic.django_ext import get_urlpatterns
    urlpatterns += get_urlpatterns("/path/to/docs", prefix="docs")
"""

from .app import create_app  # noqa: F401
from .manager import MarkdownManager  # noqa: F401

__version__ = "0.1.0"
__all__ = ["create_app", "MarkdownManager"]
