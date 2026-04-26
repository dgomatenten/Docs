"""
Command-line interface for MD Viewer.

Usage::

    md-viewer /path/to/docs
    md-viewer /path/to/docs --port 8080 --host 0.0.0.0
    python -m mdviewer /path/to/docs
"""
from __future__ import annotations

import argparse


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        prog="md-viewer",
        description="MD Viewer – serve a directory of docs in your browser.",
    )
    parser.add_argument(
        "root_dir",
        nargs="?",
        default=".",
        help="Root directory to serve (default: current directory)",
    )
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=5000, help="Port to listen on (default: 5000)")
    parser.add_argument("--debug", action="store_true", help="Enable Flask debug mode")

    args = parser.parse_args(argv)

    from .app import create_app

    app = create_app(args.root_dir)
    print(f"\n  MD Viewer")
    print(f"  Serving: {args.root_dir}")
    print(f"  URL:     http://{args.host}:{args.port}/\n")
    app.run(host=args.host, port=args.port, debug=args.debug)


if __name__ == "__main__":
    main()
