# Contributing to AI Sales Agent

Thank you for your interest in contributing to AI Sales Agent! This document provides guidelines and instructions for contributing.

## 🤝 How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:
- Clear description of the bug
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version, etc.)
- Screenshots if applicable

### Suggesting Features

Feature requests are welcome! Please:
- Check if the feature is already requested
- Clearly describe the feature and its benefits
- Provide use cases and examples

### Pull Requests

1. **Fork the repository**
   ```bash
   git clone https://github.com/yourusername/ai-sales-agent.git
   cd ai-sales-agent
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Write clean, readable code
   - Follow existing code style
   - Add comments where necessary
   - Update documentation if needed

4. **Test your changes**
   ```bash
   # Run tests
   cd backend
   pytest
   
   # Test manually
   python -m app.main
   ```

5. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add amazing feature"
   ```

   Use conventional commits:
   - `feat:` - New feature
   - `fix:` - Bug fix
   - `docs:` - Documentation changes
   - `style:` - Code style changes
   - `refactor:` - Code refactoring
   - `test:` - Test additions/changes
   - `chore:` - Maintenance tasks

6. **Push and create PR**
   ```bash
   git push origin feature/your-feature-name
   ```
   Then create a Pull Request on GitHub.

## 📝 Code Style

### Python
- Follow PEP 8
- Use type hints
- Write docstrings for functions and classes
- Maximum line length: 100 characters

```python
def example_function(param: str, count: int = 0) -> dict:
    """
    Brief description of function.
    
    Args:
        param: Description of param
        count: Description of count
        
    Returns:
        Description of return value
    """
    return {"result": param * count}
```

### JavaScript
- Use ES6+ features
- Use `const` and `let`, avoid `var`
- Use async/await for promises
- Add comments for complex logic

### Formatting Tools

```bash
# Python
pip install black flake8
black .
flake8 .

# JavaScript
npm install -g prettier
prettier --write "**/*.js"
```

## 🧪 Testing

### Running Tests

```bash
# All tests
pytest

# Specific test file
pytest tests/test_agents.py

# With coverage
pytest --cov=app tests/
```

### Writing Tests

```python
import pytest
from app.agents.research_agent import research_agent

@pytest.mark.asyncio
async def test_research_agent():
    """Test research agent functionality"""
    results = await research_agent.run(
        industry="SaaS",
        location="USA"
    )
    assert len(results) > 0
    assert results[0]["company_name"]
```

## 📚 Documentation

- Update README.md if adding features
- Add docstrings to new functions/classes
- Update API documentation if changing endpoints
- Include examples in documentation

## 🔍 Code Review Process

1. All PRs require review before merging
2. Address review comments promptly
3. Keep PRs focused and reasonably sized
4. Ensure CI/CD checks pass

## 🎯 Development Setup

### Prerequisites
- Python 3.9+
- Node.js 16+ (for frontend tools)
- Git

### Setup

```bash
# Clone repository
git clone https://github.com/yourusername/ai-sales-agent.git
cd ai-sales-agent

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
cd backend
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Development dependencies

# Install Playwright
playwright install

# Setup environment
cp .env.example .env
# Edit .env with your credentials

# Run application
python -m app.main
```

## 🐛 Debugging

### Backend
```bash
# Enable debug mode
export DEBUG=True

# Verbose logging
export LOG_LEVEL=DEBUG

# Run with debugger
python -m pdb -m app.main
```

### Frontend
- Use browser DevTools
- Check console for errors
- Use Network tab for API calls

## 📋 Project Structure

```
ai-sales-agent/
├── backend/
│   ├── app/
│   │   ├── agents/          # AI agents
│   │   ├── api/             # API routes
│   │   ├── models/          # Database models
│   │   ├── schemas/         # Pydantic schemas
│   │   ├── services/        # Business logic
│   │   ├── tools/           # Utility tools
│   │   └── utils/           # Helper functions
│   ├── tests/               # Test files
│   └── requirements.txt     # Dependencies
├── frontend/
│   ├── css/                 # Stylesheets
│   ├── js/                  # JavaScript files
│   └── index.html           # Main page
└── docs/                    # Documentation
```

## 🚀 Release Process

1. Update version in `backend/app/config.py`
2. Update CHANGELOG.md
3. Create release tag
4. Build and test
5. Create GitHub release

## 💬 Communication

- GitHub Issues - Bug reports and feature requests
- GitHub Discussions - General questions and ideas
- Pull Requests - Code contributions

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 🙏 Thank You!

Your contributions make this project better. Thank you for taking the time to contribute!
