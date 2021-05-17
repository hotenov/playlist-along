"""Sphinx configuration."""
from datetime import datetime


project = "Playlist Along"
author = "Artem Hotenov"
copyright = f"{datetime.now().year}, {author}"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_click",
    "sphinx_inline_tabs",
]
autodoc_typehints = "description"
html_theme = "furo"
