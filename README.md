# AI Base Template: Production-First AI Engineering

> Based on [A Production-First Approach to AI Engineering](https://aienhancedengineer.substack.com/p/a-production-first-approach-to-ai) - a methodology for building reliable AI systems.

## 🎯 Why This Template?

**The Problem:** Most AI projects fail when moving from prototype to production. Research notebooks that work brilliantly in development fail catastrophically under real-world conditions—latency spikes, cost spirals, non-deterministic failures, and maintenance nightmares.

**The Root Cause:** The AI industry focuses 90% on model development and 10% on the infrastructure needed for production. This ratio should be reversed. Production AI systems require engineering discipline, not just algorithmic innovation.

**The Solution:** This template provides a production-ready foundation for AI projects, embodying the principle that *"Research optimizes for possibility. Engineering optimizes for reliability."*

## 🏗️ What This Template Provides

A **modern Python foundation** designed for AI systems that need to work reliably in production:

- **Modern Python Tooling** - Python 3.12+, FastAPI, Pydantic, type hints throughout
- **Production Logging** - Structured JSON logging with correlation tracking and dual-mode rendering
- **Development Automation** - Pre-configured linting, formatting, testing, and validation
- **Production-Ready Structure** - Organized for maintainability and scaling
- **Comprehensive Testing** - Unit, functional, and integration test patterns (21+ logging tests included)
- **CI/CD Ready** - GitHub Actions, pre-commit hooks, semantic versioning
- **Documentation Standards** - Clear guides for development and deployment

This isn't another ML experiment template—it's an engineering foundation for AI systems that need to work reliably at scale.

## ⚡ Quick Start

```bash
# Clone the production-ready foundation
git clone <repository-url> my-ai-service
cd my-ai-service

# Set up the complete development environment
make init

# Verify everything works
make validate-branch
```

You now have a production-ready Python service foundation. Add your AI logic on top of this reliable base.

## 🔧 The Production-First Philosophy

### Research vs. Production Mindset

**Research Approach:**
- Optimize for accuracy and novel algorithms
- Success = high F1 scores, paper publications
- Acceptable to fail fast and iterate
- Focus on the happy path

**Production-First Approach:**
- Optimize for reliability and maintainability
- Success = uptime, cost efficiency, user satisfaction
- Must handle edge cases gracefully
- Plan for failure from the start

### The 90/10 Rule

In production AI systems:
- **10%** of your code is the actual AI/ML logic
- **90%** is infrastructure: validation, monitoring, error handling, cost controls, testing

This template provides that crucial 90% foundation.

## 🛠️ Development Workflow

### Essential Commands

```bash
# Environment management
make init              # Complete development setup
make sync              # Update dependencies  
make clean-env         # Reset environment

# Code quality
make format            # Auto-format code
make lint              # Fix linting issues
make type-check        # Validate type hints
make validate-branch   # Run all checks before committing

# Testing
make test              # Standard test suite
make test-unit         # Fast unit tests
make test-functional   # Feature tests
make test-integration  # Integration tests
make test-all          # Complete test suite
```

### Project Structure

```
ai-base-template/
├── src/                   # Your service code goes here
│   ├── __init__.py       
│   ├── main.py           # Simple starting point with logging integration
│   └── logging.py        # Production structured logging system
├── tests/                # Comprehensive test suite
│   ├── test_main.py      # Example test patterns
│   └── test_logging.py   # 21+ logging system tests
├── research/             # Notebooks and experiments
│   └── EDA.ipynb        # Exploratory work stays here
├── Makefile             # All automation commands
├── pyproject.toml       # Modern Python configuration
└── CLAUDE.md            # Detailed development guide
```

## 🎓 Who Should Use This Template

### Senior Engineers New to AI
Start with a solid engineering foundation while learning AI concepts. The template provides the safety rails you're accustomed to in production systems.

### AI Engineers Moving to Production
Stop reinventing infrastructure. Focus on your models while using battle-tested patterns for the production wrapper.

### Technical Leaders
Give your team a consistent, production-ready starting point that embodies engineering best practices from day one.

## 📊 Production Logging System

This template includes a **production-grade structured logging system** built with structlog that handles the observability requirements of real-world AI systems.

### Dual-Mode Logging

**Development Mode** - Human-readable format for debugging:
```bash
22:45:00 [INFO] main: Processing request [HTTP 200, 150ms, user_id=user-123] [id:req-abc12]
```

**Production Mode** - Structured JSON for monitoring systems:
```json
{
  "timestamp": "2025-08-31T22:45:00.123Z",
  "level": "info", 
  "logger": "main",
  "message": "Processing request",
  "context": "default",
  "extra": {
    "status_code": 200,
    "duration_ms": 150,
    "user_id": "user-123",
    "correlation_id": "req-abc-123"
  }
}
```

### Built-in Features

- **Correlation ID Tracking** - Trace requests across your entire system
- **Context Isolation** - Prevent data leakage between concurrent requests
- **Smart Field Organization** - Important fields (status_code, duration_ms) formatted for readability
- **Environment-Driven Configuration** - `LOGGING_LEVEL` and `LITELLM_LOG_LEVEL` support
- **Logger Name Abbreviation** - Clean, readable logger names in development

### Usage Example

```python
from src.logging import configure_structlog, get_logger, bind_contextvars

# Configure for your environment
configure_structlog(testing=False)  # Production JSON output
logger = get_logger(__name__)

# Bind correlation ID at request start
bind_contextvars(correlation_id="req-123", user_id="user-456")

# All subsequent logs will include context automatically
logger.info("Processing AI request", model="gpt-4", tokens=150)
logger.info("Request completed", status_code=200, duration_ms=1200)
```

### Integration with AI Systems

The logging system is specifically designed for AI/ML production requirements:
- **Cost tracking** with built-in fields for model usage
- **Performance monitoring** with latency and token usage
- **Request tracing** across complex AI pipelines
- **Error categorization** for model vs. infrastructure failures

## 📚 Learn More

### Core Methodology
- [A Production-First Approach to AI Engineering](https://aienhancedengineer.substack.com/p/a-production-first-approach-to-ai) - The article that inspired this template

### Production AI Engineering
- [Google's Rules for ML](https://developers.google.com/machine-learning/guides/rules-of-ml) - Engineering discipline for ML systems
- [Hidden Technical Debt in ML Systems](https://papers.nips.cc/paper/5656-hidden-technical-debt-in-machine-learning-systems.pdf) - Foundational NIPS paper

### Technologies Used
- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [Pydantic](https://docs.pydantic.dev/) - Data validation using type annotations
- [structlog](https://www.structlog.org/) - Structured logging for production systems
- [uv](https://docs.astral.sh/uv/) - Modern Python package management

## 🤝 Contributing

This template embodies battle-tested patterns from production AI systems. When contributing, prioritize:

1. **Reliability over features**
2. **Simplicity over cleverness**
3. **Documentation over assumptions**
4. **Tests over trust**

## 📄 License

Apache License 2.0 - See [LICENSE](LICENSE) file for details.

---

**Remember:** The hardest part of AI isn't the algorithms—it's making them work reliably in production. This template gives you a head start on that challenge.

*"The best AI is the AI that works."*
