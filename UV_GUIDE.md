# Using uv with Spotify-Advance

[uv](https://github.com/astral-sh/uv) is a fast Python package installer and resolver that can drastically speed up your Python development workflow. This guide explains how to use uv with this project.

## Installation

Install uv using one of these methods:

```bash
# Using the install script
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or using pip
pip install uv
```

## Setting up the environment

Create a new virtual environment with uv:

```bash
# Create a virtual environment
uv venv

# Activate it
source .venv/bin/activate  # On Unix/macOS
# or
.venv\Scripts\activate     # On Windows
```

## Installing dependencies

### Install all required dependencies

```bash
# Install using pyproject.toml
uv sync
```

### Install with development dependencies

```bash
# Install in development mode with dev dependencies
uv pip install -e ".[dev]"
```

### Add a new dependency

```bash
# Add a new package
uv pip install new-package

# Update pyproject.toml manually to include this dependency
```

## Migrating from pip

If you're used to pip commands, here are the uv equivalents:

| pip command | uv command |
|-------------|------------|
| `pip install -r requirements.txt` | `uv pip install -r requirements.txt` |
| `pip install package` | `uv pip install package` |
| `pip install -e .` | `uv pip install -e .` |
| `pip freeze > requirements.txt` | `uv pip freeze > requirements.txt` |

## Benefits of uv

- **Speed**: uv is 10-100x faster than pip for installations
- **Better dependency resolution**: More reliable dependency solving
- **PEP 621 support**: Works with modern pyproject.toml configuration
- **Caching**: Efficient caching for faster repeated installs
- **Virtual environments**: Built-in virtual environment management

## Troubleshooting

If you encounter issues:

1. Make sure your Python version matches the project requirement (Python 3.10+)
2. Check that the pyproject.toml file has valid syntax
3. Run `uv --version` to verify uv is installed correctly
4. For detailed logs, use `uv --verbose sync` 