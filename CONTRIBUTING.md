# Contributing to TermNexus

Thank you for your interest in contributing to TermNexus! We welcome contributions from the community.

## How to Contribute

### Reporting Issues

- Use the [GitHub Issues](https://github.com/gitstq/TermNexus/issues) page
- Provide a clear description of the problem
- Include steps to reproduce
- Mention your operating system and Python version

### Submitting Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`python -m unittest discover tests/`)
5. Commit with clear messages following [Conventional Commits](https://www.conventionalcommits.org/)
6. Push to your fork
7. Open a Pull Request

### Commit Message Format

```
feat: add new workspace tagging feature
fix: resolve session detection on macOS
docs: update README with new examples
refactor: simplify workspace manager logic
test: add router module tests
```

### Code Style

- Follow PEP 8 guidelines
- Use type hints where appropriate
- Add docstrings to all public functions and classes
- Keep functions focused and modular

### Testing

- Write tests for new features
- Ensure all tests pass before submitting PR
- Aim for high test coverage

## Development Setup

```bash
git clone https://github.com/gitstq/TermNexus.git
cd TermNexus
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e .
python -m unittest discover tests/
```

## Code of Conduct

Be respectful and constructive in all interactions.
