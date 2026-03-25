# Configuration file for the Sphinx documentation builder.

project = "LED Stripe Controller"
copyright = "2026, LED vX Project"
author = "LED vX Project"
release = "0.1.0"

extensions = [
    "sphinx_needs",
]

# Sphinx-needs configuration
needs_types = [
    {
        "directive": "req",
        "title": "Requirement",
        "prefix": "REQ_",
        "color": "#BFD8D2",
        "style": "node",
    },
    {
        "directive": "spec",
        "title": "Specification",
        "prefix": "SPEC_",
        "color": "#FEDCD2",
        "style": "node",
    },
    {
        "directive": "arch",
        "title": "Architecture Element",
        "prefix": "ARCH_",
        "color": "#DF744A",
        "style": "node",
    },
    {
        "directive": "comp",
        "title": "Component",
        "prefix": "COMP_",
        "color": "#DCB239",
        "style": "node",
    },
    {
        "directive": "iface",
        "title": "Interface",
        "prefix": "IFACE_",
        "color": "#9856a5",
        "style": "node",
    },
]

needs_fields = {
    "rationale": {
        "description": "Rationale for the requirement or design decision.",
        "nullable": True,
    },
    "language": {
        "description": "Implementation language (e.g. C++17, Python).",
        "nullable": True,
    },
    "layer": {
        "description": "Architectural layer (realtime, highlevel, hal).",
        "nullable": True,
    },
}

needs_id_regex = r"^[A-Z]+_[A-Z0-9_]+"

html_theme = "alabaster"
html_static_path = []

exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
