# Configuration file for Sphinx documentation builder.
# pytop API Reference — auto-generated documentation

project = "pytop"
copyright = "2024, Kadirhan Polat"
author = "Kadirhan Polat"

import sys
from pathlib import Path

# Add src to path for autodoc
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

release = "1.6.0"
version = "1.6"

# Extensions
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
    "sphinx.ext.mathjax",
    "sphinx_rtd_theme",
]

# Autodoc settings
autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "show-inheritance": True,
    "member-order": "bysource",
}

autosummary_generate = True

# Theme
html_theme = "sphinx_rtd_theme"

html_theme_options = {
    "display_version": True,
    "prev_next_buttons_location": "bottom",
    "style_external_links": False,
    "logo_only": False,
}

html_static_path = ["_static"]
html_css_files = []

# Output options
html_copy_source = True
html_show_sourcelink = True
html_show_sphinx = True

# Master document
master_doc = "index"

# Exclude patterns
exclude_patterns = ["_build", "_templates"]

# Language
language = "en"

# Mathematical notation
mathjax_config = {
    "tex": {"inlineMath": [["$", "$"], ["\\(", "\\)"]]},
    "chtml": {"displayAlign": "center"},
}

# Intersphinx mappings
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}
