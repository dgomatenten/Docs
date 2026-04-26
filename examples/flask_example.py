# Kinetic MD Viewer — example Flask integration
from flask import Flask
from mdviewer.flask_ext import create_blueprint

app = Flask(__name__)

# Mount the Markdown viewer at /docs/
# Change the path to any directory with .md files
docs_blueprint = create_blueprint("./docs_example")
app.register_blueprint(docs_blueprint, url_prefix="/docs")

@app.route("/")
def home():
    return '<h2>My App</h2><p><a href="/docs/">Open Docs</a></p>'


if __name__ == "__main__":
    import os, pathlib
    # Create a sample docs dir for the demo
    sample = pathlib.Path("docs_example")
    sample.mkdir(exist_ok=True)
    (sample / "README.md").write_text("# Welcome\n\nThis is your documentation root.\n")
    (sample / "guide.md").write_text(
        "# Guide\n\n## Installation\n\nRun `pip install kinetic-md-viewer`.\n\n"
        "## Usage\n\nImport and register the blueprint.\n"
    )
    print("Flask app running — visit http://127.0.0.1:5000/docs/")
    app.run(debug=True)
