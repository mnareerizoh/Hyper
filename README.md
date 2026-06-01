# Hyper

A professional Python project built with best practices for testing and CI/CD.

## Overview

Hyper is designed to be a scalable, well-tested Python application with automated quality checks and deployment pipelines.

## Features

- ✅ Automated testing with pytest
- ✅ Code quality checks (linting, formatting)
- ✅ CI/CD with GitHub Actions
- ✅ Type hints and mypy checking
- ✅ Professional project structure

## Quick Start

### Prerequisites

- Python 3.9+
- pip or uv

### Installation

```bash
# Clone the repository
git clone https://github.com/mnareerizoh/Hyper.git
cd Hyper

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e ".[dev]"
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=hyper

# Run specific test file
pytest tests/test_example.py
```

### Code Quality

```bash
# Format code
black hyper/ tests/

# Lint code
flake8 hyper/ tests/

# Type checking
mypy hyper/
```

## Project Structure

```
Hyper/
├── hyper/                 # Main package
│   ├── __init__.py
│   ├── core.py           # Core functionality
│   └── utils.py          # Utility functions
├── tests/                # Test files
│   ├── __init__.py
│   ├── test_core.py
│   └── test_utils.py
├── .github/
│   └── workflows/        # GitHub Actions
├── pyproject.toml        # Project configuration
├── README.md            # This file
├── .gitignore           # Git ignore rules
└── CONTRIBUTING.md      # Contribution guidelines
```

## Development

See [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines.

## License

MIT License - See LICENSE file for details

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) first.

---

**Built with Python, pytest, and GitHub Actions** 🚀
