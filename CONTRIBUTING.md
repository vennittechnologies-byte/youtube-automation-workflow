# Contributing to YouTube Automation Workflow

First off, thank you for considering contributing to this project! 🎉

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates. When creating a bug report, include:

- **Clear title and description**
- **Steps to reproduce** the behavior
- **Expected vs actual behavior**
- **Screenshots** if applicable
- **Environment details** (OS, Python version, etc.)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:

- **Clear title and description**
- **Use case** - why is this enhancement useful?
- **Possible implementation** if you have ideas
- **Examples** from other projects if applicable

### Pull Requests

1. **Fork the repository** and create your branch from `main`
2. **Follow the existing code style**
3. **Test your changes** thoroughly
4. **Update documentation** if needed
5. **Write clear commit messages**
6. **Submit the pull request**

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/youtube-automation-workflow.git
cd youtube-automation-workflow

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest black flake8 mypy

# Run tests
pytest tests/

# Format code
black .

# Lint
flake8 scripts/
```

## Code Style

- Follow **PEP 8** style guide
- Use **type hints** where appropriate
- Write **docstrings** for functions and classes
- Keep functions **small and focused**
- Use **meaningful variable names**

Example:

```python
def generate_script(topic: str, duration: int = 60) -> Dict[str, str]:
    """
    Generate a video script for the given topic.
    
    Args:
        topic: The topic/subject for the video
        duration: Target duration in seconds (default: 60)
        
    Returns:
        Dictionary containing title, script, and metadata
    """
    # Implementation
    pass
```

## Testing

- Write tests for new features
- Ensure all tests pass before submitting PR
- Aim for good test coverage

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_script_generator.py

# Run with coverage
pytest --cov=scripts tests/
```

## Documentation

- Update README.md for significant changes
- Add docstrings to new functions/classes
- Update QUICKSTART.md if setup process changes
- Create examples for new features

## Commit Messages

Write clear, concise commit messages:

```
feat: Add subtitle generation feature
fix: Resolve video encoding issue on Windows
docs: Update YouTube OAuth setup instructions
refactor: Simplify video composition logic
test: Add tests for thumbnail generator
```

Prefixes:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation
- `refactor:` - Code refactoring
- `test:` - Testing
- `chore:` - Maintenance

## Areas for Contribution

Looking for ideas? Here are some areas that need work:

### High Priority
- [ ] Automated testing suite
- [ ] Better error handling
- [ ] Performance optimization
- [ ] Cross-platform compatibility (Windows testing)

### Medium Priority
- [ ] Subtitle/caption generation
- [ ] Multiple voice support (dialogue)
- [ ] AI image generation integration
- [ ] Video analytics tracking
- [ ] Custom video effects

### Low Priority
- [ ] Web UI interface
- [ ] Docker containerization
- [ ] Alternative LLM providers
- [ ] More stock footage sources

## Questions?

Feel free to ask questions in:
- GitHub Issues (for bugs/features)
- GitHub Discussions (for general questions)

## Code of Conduct

Be respectful and considerate. We're all here to learn and improve.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing! 🚀
