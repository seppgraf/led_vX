# led_vX
Project to control LED Stripes

## Development with GitHub Codespaces

This repository includes a devcontainer configuration for
[GitHub Codespaces](https://github.com/features/codespaces) so you can build
and view the Sphinx documentation without any local setup.

### Opening in Codespaces

1. Click **Code → Codespaces → New codespace** on the repository page.
2. Wait for the container to build. Python dependencies (`sphinx`,
   `sphinx-needs`) are installed automatically.

### Building the documentation

From the repository root, run:

```bash
sphinx-build -b html docs docs/_build/html
```

### Viewing the documentation

Start a local web server to browse the built HTML:

```bash
python -m http.server 8000 --directory docs/_build/html
```

The Codespace automatically forwards port **8000**. Open the link shown in the
**Ports** tab (or the pop-up notification) to view the documentation in your
browser.
