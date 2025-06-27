# fluree-py

<div align="center">

[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Documentation](https://img.shields.io/badge/docs-latest-blue.svg)](https://crcresearch.github.io/fluree-py/)

A Python client library for interacting with FlureeDB, providing a type-safe and developer-friendly interface to the FlureeDB API.

[Documentation](https://crcresearch.github.io/fluree-py/) • [Report Bug](https://github.com/crcresearch/fluree-py/issues) • [Request Feature](https://github.com/crcresearch/fluree-py/issues)

</div>

## 📑 Table of Contents

- [Features](#-features)
- [Quick Start](#-quick-start)
  - [Installation](#installation)
  - [Basic Usage](#basic-usage)
  - [Advanced Usage](#advanced-usage)
- [Architecture](#-architecture)
- [Development](#-development)
  - [Setup Development Environment](#setup-development-environment)
  - [Running Tests](#running-tests)
  - [Building Documentation](#building-documentation)
  - [Code Style](#code-style)
- [Dependencies](#-dependencies)
- [Release Process](#-release-process)
- [Roadmap](#-roadmap)
- [License](#-license)
- [Contributing](#-contributing)
- [Author](#-author)
- [Acknowledgments](#-acknowledgments)

## ✨ Features

- 🔒 Type-safe API interactions using Pydantic models
- ⚡ Modern async/await HTTP client using `httpx`
- 🔄 Support for both synchronous and asynchronous operations
- 📝 Full type hints support
- ✅ Extensive test coverage with pytest and hypothesis
- 📚 Detailed documentation with MkDocs
- 🚀 Fast and efficient with `uv` package management
- 🧹 Clean code with `ruff` linting and formatting

## 🚀 Quick Start

### Installation

```bash
pip install git+https://github.com/crcresearch/fluree-py.git
```

### Basic Usage

The library supports both synchronous and asynchronous operations. Here's an example showing both approaches:

```python
from fluree_py import FlureeClient

# Initialize the client
client = FlureeClient(url="http://localhost:8090")

# Create a ledger with initial data
to_commit = (
    client.with_ledger("example/ledger")
    .create()
    .with_context(
        {
            "ex": "http://example.org/",
            "schema": "http://schema.org/",
        }
    )
    .with_insert(
        {
            "@id": "ex:freddy",
            "@type": "ex:Yeti",
            "schema:age": 4,
            "schema:name": "Freddy",
        }
    )
)

# Synchronous commit operation
response = to_commit.commit()
print("Sync response:", response.json())

# Asynchronous commit operation
response = await to_commit.acommit()
print("Async response:", response.json())
```

## 🏗️ Architecture

The library is built with a modular architecture:

- `fluree_py/http/` - HTTP client implementation using `httpx`
- `fluree_py/types/` - Type definitions and Pydantic models

## 🛠️ Development

This project uses modern Python development tools and practices:

- 🚀 `uv` for build and package management
- 🔍 `pytest` for testing
- 🧹 `ruff` for linting
- 📚 `mkdocs` for documentation
- 🔄 `hypothesis` for property-based testing

### Setup Development Environment

1. Clone the repository:
```bash
git clone https://github.com/crcresearch/fluree-py.git
cd fluree-py
```

2. Install development dependencies:
```bash
uv sync --all-extras --dev
```

### Running Tests

```bash
uv run pytest
```

### Building Documentation

```bash
uv run mkdocs build
```

### Code Style

This project follows the following code style guidelines:

- Use `ruff` for linting and formatting
- Follow PEP 8 guidelines
- Use type hints for all function parameters and return values
- Use docstrings for all public functions and classes
- Use meaningful variable and function names
- Keep functions focused and small

## 📦 Dependencies

Core dependencies:
- Python >= 3.11
- httpx >= 0.28.1
- pydantic >= 2.10.6

Development dependencies:
- uv
- pytest
- ruff
- mkdocs
- hypothesis

## 🚀 Release Process

1. Update version in `pyproject.toml`
2. Update CHANGELOG.md
3. Create a new release on GitHub
4. Build and publish to PyPI

## 🗺️ Roadmap

- [ ] Implement query builder
- [ ] Improve error handling and messages
- [ ] Improve documentation, examples and tutorials

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 👤 Author

- **James Sweet** - [jsweet@nd.edu](mailto:jsweet@nd.edu)

## 🙏 Acknowledgments

- [FlureeDB](https://flur.ee/) - The underlying database this client connects to
- [httpx](https://github.com/encode/httpx) - The HTTP client library used
- [Pydantic](https://github.com/pydantic/pydantic) - For type-safe data validation
