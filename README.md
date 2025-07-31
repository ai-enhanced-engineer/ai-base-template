# AI Base Template

A modern Python template for ML/AI projects with FastAPI, designed for rapid prototyping with production-ready architecture.

## Features

- 🚀 **FastAPI** for high-performance REST APIs
- 🧪 **Full testing setup** with pytest (unit, functional, integration)
- 🔧 **Modern tooling** with uv, Ruff, and MyPy
- 📊 **ML-ready** with scikit-learn, XGBoost, PyTorch pre-configured
- 🐳 **Docker-ready** architecture
- 📝 **Type-safe** with Pydantic models and strict MyPy checking
- 🔍 **Observable** with structured logging via loguru
- ⚡ **Fast development** with Make commands for common tasks

## Quick Start

### Prerequisites
- Python 3.12+
- Make

### Setup

1. Clone this template:
```bash
git clone <repository-url>
cd ai-base-template
```

2. Create environment and install dependencies:
```bash
make environment-create
```

3. Run the development server:
```bash
uvicorn ai_base_template.main:app --reload
```

4. Visit http://localhost:8000/docs for the interactive API documentation

## Project Structure

```
ai-base-template/
├── ai_base_template/      # Main application code
│   ├── __init__.py
│   └── main.py           # FastAPI application
├── tests/                # Test suite
│   └── test_main.py      # Example tests
├── research/             # Notebooks and experiments
│   └── EDA.ipynb        # Exploratory data analysis
├── testing/              # API testing utilities
├── Makefile             # Development automation
├── pyproject.toml       # Project dependencies
├── CLAUDE.md            # Development guide
└── README.md            # This file
```

## Development Workflow

### Common Commands

```bash
# Environment management
make environment-create   # Initial setup
make environment-sync     # Update dependencies

# Code quality
make format              # Auto-format code
make lint               # Lint and fix issues
make type-check         # Run type checking
make validate-branch    # Run all checks

# Testing
make unit-test          # Run unit tests
make functional-test    # Run functional tests
make all-test          # Run all tests with coverage
```

### Writing Code

1. Add your code to `ai_base_template/`
2. Write tests in `tests/`
3. Use `make validate-branch` before committing
4. Follow the conventions in CLAUDE.md

## Technology Stack

### Core
- **FastAPI** - Modern web framework
- **Pydantic** - Data validation
- **uvicorn** - ASGI server

### ML/Data Science
- **scikit-learn** - Classical ML
- **XGBoost/LightGBM** - Gradient boosting
- **PyTorch** - Deep learning
- **pandas/numpy** - Data manipulation
- **SHAP** - Model interpretability

### Development
- **uv** - Fast package manager
- **Ruff** - Linter and formatter
- **MyPy** - Static type checker
- **pytest** - Testing framework
- **pre-commit** - Git hooks

## Configuration

Configuration is handled through environment variables and Pydantic settings. Create a `.env` file for local development:

```env
# Example .env file
API_KEY=your-api-key
MODEL_PATH=./models
LOG_LEVEL=DEBUG
```

## Testing

The template includes a comprehensive testing setup:

- **Unit tests**: Test individual components
- **Functional tests**: Test complete workflows
- **Integration tests**: Test with external dependencies

Run tests with coverage:
```bash
make all-test
```

## Best Practices

- ✅ Type hints on all functions
- ✅ Pydantic models for validation
- ✅ Structured logging
- ✅ Environment-based config
- ✅ No hardcoded secrets
- ✅ >80% test coverage
- ✅ Pre-commit hooks

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run `make validate-branch`
5. Submit a pull request

## License

[Your License Here]

## Support

For issues and questions:
- Check the [CLAUDE.md](./CLAUDE.md) development guide
- Open an issue on GitHub
- Review the example code in `ai_base_template/`

---

Built with ❤️ for modern ML/AI development