"""
Standalone Flask application factory.
Can be used directly via CLI or imported as part of any Flask project.
"""
from __future__ import annotations

import os
from pathlib import Path

from flask import Flask

from .flask_ext import create_blueprint


def create_app(root_dir: str | os.PathLike | None = None, **flask_kwargs) -> Flask:
    """
    Create and return a configured Flask application.

    Parameters
    ----------
    root_dir : str | Path | None
        Directory to serve.  Defaults to the current working directory.
    flask_kwargs :
        Extra keyword arguments passed to :class:`flask.Flask`.

    Example::

        from kinetic import create_app
        app = create_app("/my/docs")
        app.run(debug=True)
    """
    root_dir = Path(root_dir or os.getcwd()).resolve()

    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static",
        **flask_kwargs,
    )
    app.secret_key = os.environ.get("KINETIC_SECRET", "kinetic-dev-secret")

    blueprint = create_blueprint(root_dir)
    app.register_blueprint(blueprint)

    return app
