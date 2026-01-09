# Python Agentic Template

> Describe what you want to build. Let agents build it.

Autonomous multi-agent Python project template.

## Why This Template?

**The Problem:** Starting AI/ML projects requires extensive setup—architecture decisions, project structure, testing patterns, CI/CD, logging, and more. Most developers copy-paste from old projects or spend days configuring from scratch.

**The Solution:** This template **bootstraps itself** into a complete, production-ready project through a multi-agent workflow. You describe your project in plain language; agents research, plan, and build it.

## How It Works

```
┌─────────────────────────────────────────────────────────────────┐
│  YOU: Fill context/PRODUCT.md + context/ENGINEERING.md         │
│       (Describe what you're building and technical preferences) │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  PHASE 0: Agent Discovery                                       │
│           Claude Code finds available specialists and maps      │
│           them to roles (research, architecture, implementation,│
│           review)                                               │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  PHASE 1: Research                                              │
│           Expands your seeds into full PRD                      │
│           Researches best practices, grades evidence            │
│           → context/PRD.md, context/RESEARCH_SYNTHESIS.md       │
└─────────────────────────────────────────────────────────────────┘
                              ↓ [User Approval]
┌─────────────────────────────────────────────────────────────────┐
│  PHASE 2: Architecture                                          │
│           Creates ADRs and project plan                         │
│           Defines MVP scope with MoSCoW prioritization          │
│           → ADR.md, context/PROJECT_PLAN.md                     │
└─────────────────────────────────────────────────────────────────┘
                              ↓ [User Approval]
┌─────────────────────────────────────────────────────────────────┐
│  PHASE 3: MVP Implementation                                    │
│           Builds must-have features with tests                  │
│           Per deliverable: IMPLEMENT → REVIEW → FIX → PASS      │
│           Review enforces 80% coverage, test quality            │
│           → Working code in src/                                │
└─────────────────────────────────────────────────────────────────┘
                              ↓ [User Approval]
┌─────────────────────────────────────────────────────────────────┐
│  PHASE 4: Feature Enhancement                                   │
│           Adds features from roadmap (same validation loop)     │
│           Each feature: IMPLEMENT → REVIEW → FIX → User Approval│
└─────────────────────────────────────────────────────────────────┘
```

**Human-in-the-loop**: You approve each phase before continuing. No runaway automation.

## Quick Start

1. **Create your repository**: Click "Use this template" on GitHub
2. **Set up environment**: `just init`
3. **Fill out your seeds**: Edit `context/PRODUCT.md` and `context/ENGINEERING.md`
4. **Start brewing**: In Claude Code, say `"Run the project initialization workflow"`

### Filling Out Seeds

| File | What to Include |
|------|-----------------|
| `context/PRODUCT.md` | What you're building, for whom, why, success criteria |
| `context/ENGINEERING.md` | Technical preferences, constraints, architecture ideas |

**Tips for better results**:
- Be specific about the problem: "Users waste 2 hours/day on X" > "Users have problems"
- Define success measurably: "50% reduction in Y" > "Improve Y"
- State constraints clearly: "Must run on GCP" > "Cloud deployment"

See `workflows/PROJECT_INIT_WORKFLOW.md` for the complete workflow specification.

## What You Get

Beyond the autonomous workflow, this template provides a **production-ready foundation**:

### Modern Python Tooling
- Python 3.12+, FastAPI, Pydantic
- Type hints throughout
- uv for fast dependency management

### Production Logging
- Structured JSON logging with structlog
- Correlation ID tracking across requests
- Dual-mode: human-readable (dev) / JSON (prod)

### Development Automation
- Pre-configured linting (Ruff), formatting (Black), type checking (mypy)
- Pre-commit hooks for quality gates
- `just validate-branch` runs all checks

### Testing Patterns
- Unit, functional, and integration test structure
- pytest with markers for test organization
- 21+ logging system tests included as examples

### CI/CD Ready
- GitHub Actions workflows
- Semantic versioning
- Docker-ready structure

## Project Structure

```
my-project/
├── context/                   # Project seeds + workflow outputs
│   ├── PRODUCT.md             # Your product requirements (seed)
│   ├── ENGINEERING.md         # Your technical preferences (seed)
│   ├── PRD.md                 # Expanded PRD (generated)
│   ├── RESEARCH_SYNTHESIS.md  # Research findings (generated)
│   └── PROJECT_PLAN.md        # MVP scope + roadmap (generated)
├── workflows/                 # Autonomous workflow system
│   ├── PROJECT_INIT_WORKFLOW.md  # Complete workflow specification
│   └── templates/             # Output format contracts
├── src/                       # Your service code
│   ├── __init__.py
│   ├── main.py                # Entry point with logging demo
│   └── logging.py             # Production logging system
├── tests/                     # Test suite
│   ├── test_main.py
│   └── test_logging.py        # 21+ logging tests
├── research/                  # Notebooks and experiments
├── ADR.md                     # Architecture decisions (generated)
├── justfile                   # All automation commands
└── pyproject.toml             # Project configuration
```

## Development Commands

```bash
just                   # Show all available commands

# Environment
just init              # Complete development setup
just sync              # Update dependencies
just clean-env         # Reset environment

# Code Quality
just format            # Auto-format code
just lint              # Fix linting issues
just type-check        # Validate type hints
just validate-branch   # Run all checks (required before commits)

# Testing
just test              # Standard test suite
just test-unit         # Fast unit tests
just test-functional   # Feature tests
just test-integration  # Integration tests
just test-all          # Complete test suite
```

## The Production-First Philosophy

This template embodies the principle that **production AI requires engineering discipline**:

- **90% infrastructure, 10% model code**: Most production AI is validation, monitoring, error handling, and cost controls—not algorithms
- **Reliability over novelty**: Production systems must work consistently, not just impressively
- **Plan for failure**: Every external call needs error handling; every assumption needs validation

The autonomous workflow ensures these patterns are built in from the start, not bolted on later.

## Who Should Use This

### Teams Starting AI/ML Projects
Stop reinventing infrastructure. Describe your project and let agents build a production-ready foundation.

### Senior Engineers New to AI
Get the safety rails you're accustomed to in production systems while learning AI concepts.

### Technical Leaders
Give your team a consistent, production-ready starting point that embodies engineering best practices.

## Learn More

### This Template
- `workflows/PROJECT_INIT_WORKFLOW.md` - Complete workflow specification
- `workflows/templates/` - Output format examples

### Production AI Engineering
- [A Production-First Approach to AI Engineering](https://aienhancedengineer.substack.com/p/a-production-first-approach-to-ai)
- [Google's Rules for ML](https://developers.google.com/machine-learning/guides/rules-of-ml)
- [Hidden Technical Debt in ML Systems](https://papers.nips.cc/paper/5656-hidden-technical-debt-in-machine-learning-systems.pdf)

### Technologies
- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [Pydantic](https://docs.pydantic.dev/) - Data validation
- [structlog](https://www.structlog.org/) - Structured logging
- [uv](https://docs.astral.sh/uv/) - Fast Python package management

## Contributing

When contributing, prioritize:
1. **Reliability over features**
2. **Simplicity over cleverness**
3. **Documentation over assumptions**
4. **Tests over trust**

## License

Apache License 2.0 - See [LICENSE](LICENSE) file.

---

*"Describe what you want. Let agents build it."*
