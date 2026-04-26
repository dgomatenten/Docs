# MD Viewer — example Django integration
"""
Add to your Django project:

1. pip install md-viewer django
2. Add mdviewer template dir to TEMPLATES in settings.py
3. Include the URL patterns in urls.py (see below)
"""

# ── urls.py ────────────────────────────────────────────────────────────────
from django.contrib import admin
from django.urls import path
from mdviewer.django_ext import get_urlpatterns

urlpatterns = [
    path("admin/", admin.site.urls),

    # Mount the Markdown viewer at /docs/
    # Change the first argument to your docs directory
    *get_urlpatterns("./docs_example", prefix="docs"),
]

# ── settings.py additions ─────────────────────────────────────────────────
# In your TEMPLATES setting, add the mdviewer templates dir:
#
# import mdviewer
# import pathlib
# MDVIEWER_TMPL = str(pathlib.Path(mdviewer.__file__).parent / "templates")
#
# TEMPLATES = [{
#     "BACKEND": "django.template.backends.django.DjangoTemplates",
#     "DIRS": [MDVIEWER_TMPL],
#     ...
# }]
