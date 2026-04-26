# MD Viewer

A premium Markdown documentation viewer for Python — use it as a **standalone app** or integrate it into **Flask** or **Django**.

## Features

- 📂 **File tree sidebar** with collapsible directories
- 📄 **GitHub-flavoured Markdown** rendering (tables, task lists, footnotes, code highlights, admonitions, and more)
- 🔍 **Live full-text search** across all Markdown files
- 📑 **Table of Contents** with scroll-spy
- 📋 **Copy-code** buttons on all code blocks
- 🖱️ **Resizable sidebar** via drag handle
- 🌙 **Premium dark theme** — glassmorphism topbar, syntax highlighting

---

## Installation

```bash
git clone <repo>
cd tool
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

---

## Usage

### Standalone (CLI)

```bash
md-viewer /path/to/your/docs
# or
python -m mdviewer /path/to/your/docs --port 8080 --debug
```

### Flask Integration

```python
from flask import Flask
from mdviewer.flask_ext import create_blueprint

app = Flask(__name__)
bp = create_blueprint("/path/to/docs")
app.register_blueprint(bp, url_prefix="/docs")

if __name__ == "__main__":
    app.run(debug=True)
```

### Django Integration

```python
# settings.py — add mdviewer templates directory
import mdviewer, pathlib
MDVIEWER_TMPL = str(pathlib.Path(mdviewer.__file__).parent / "templates")
TEMPLATES[0]["DIRS"] += [MDVIEWER_TMPL]

# urls.py
from mdviewer.django_ext import get_urlpatterns

urlpatterns = [
    path("admin/", admin.site.urls),
    *get_urlpatterns("/path/to/docs", prefix="docs"),
]
```

### Python API

```python
from mdviewer import MarkdownManager

manager = MarkdownManager("/path/to/docs")

# Render a file
result = manager.render("guide/quickstart.md")
print(result["html"])
print(result["toc"])

# Get file tree
tree = manager.get_tree()

# Search
hits = manager.search("installation")
```

---

## Project Structure

```
mdviewer/
├── __init__.py       # Public API
├── __main__.py       # python -m mdviewer
├── cli.py            # CLI entry point
├── manager.py        # Core: file scanning & rendering
├── app.py            # Standalone Flask app factory
├── flask_ext.py      # Flask Blueprint
├── django_ext.py     # Django views & URL patterns
├── templates/
│   └── mdviewer/
│       └── viewer.html
└── static/
    └── css/
        └── viewer.css
```
