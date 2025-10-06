# Contributing to Politician Trade Tracker

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue with:
- A clear description of the problem
- Steps to reproduce the issue
- Expected behavior vs actual behavior
- Your environment (OS, Python version, Docker version)
- Relevant log output (with sensitive info redacted)

### Suggesting Features

Feature requests are welcome! Please open an issue describing:
- The problem you're trying to solve
- Your proposed solution
- Any alternatives you've considered
- Whether you're willing to help implement it

### Pull Requests

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/your-feature-name`
3. **Make your changes**
4. **Test thoroughly**: Ensure the app still works
5. **Commit with clear messages**: `git commit -m "Add feature: description"`
6. **Push to your fork**: `git push origin feature/your-feature-name`
7. **Open a Pull Request**

## Development Setup

### Prerequisites

- Python 3.11+
- Docker and Docker Compose (for container testing)
- Git

### Local Development

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/politician-trade-tracker.git
cd politician-trade-tracker

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env
# Edit .env with your test credentials

# Run the app
python app/main.py --once
```

### Testing Changes

Before submitting a PR:

1. **Test locally**: Run `python app/main.py --once`
2. **Test with Docker**:
   ```bash
   docker-compose build
   docker-compose up
   ```
3. **Check for errors**: Review logs for any issues
4. **Test email notifications**: Ensure emails still send correctly

## Code Guidelines

### Python Style

- Follow [PEP 8](https://pep8.org/) style guide
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and concise

### Code Structure

```python
def function_name(param: str) -> bool:
    """Brief description of what the function does.

    Args:
        param: Description of parameter

    Returns:
        Description of return value
    """
    # Implementation
    return True
```

### Commit Messages

- Use present tense: "Add feature" not "Added feature"
- Be descriptive but concise
- Reference issues: "Fix #123: Description"

Examples:
- ✅ `Add support for House representatives`
- ✅ `Fix email encoding issue for special characters`
- ✅ `Update README with troubleshooting steps`
- ❌ `Fixed stuff`
- ❌ `Update`

## Areas for Contribution

### High Priority

- [ ] Support for additional data sources
- [ ] Web dashboard for viewing tracked trades
- [ ] SMS/Telegram notifications
- [ ] More robust error handling and retry logic
- [ ] Unit tests and integration tests

### Medium Priority

- [ ] Support for filtering by transaction size
- [ ] Trade analytics and insights
- [ ] Multiple email recipient support
- [ ] Slack/Discord webhook integration
- [ ] Better logging and monitoring

### Low Priority

- [ ] GraphQL API
- [ ] Mobile app
- [ ] Historical trade analysis
- [ ] Portfolio tracking features

## Project Structure

```
politician-trade-tracker/
├── app/
│   ├── __init__.py
│   ├── main.py           # Main application logic
│   ├── models.py         # Database models
│   ├── config.py         # Configuration management
│   └── email_service.py  # Email notifications
├── data/                 # SQLite database (gitignored)
├── config.yaml           # App configuration
├── .env.example          # Environment template
├── requirements.txt      # Python dependencies
├── Dockerfile            # Container image
├── docker-compose.yml    # Docker orchestration
└── README.md             # Main documentation
```

## Adding New Features

### Example: Adding Slack Notifications

1. **Create new service file**: `app/slack_service.py`
2. **Add configuration**: Update `config.yaml` schema
3. **Update main.py**: Integrate the new service
4. **Add dependencies**: Update `requirements.txt`
5. **Document**: Update README and SETUP_GUIDE
6. **Test**: Verify it works end-to-end

### Example: Supporting House Representatives

1. **Research data source**: Find reliable House disclosure data
2. **Update models**: Add any new fields needed
3. **Update fetcher**: Modify `fetch_trades()` in main.py
4. **Test**: Verify House members are tracked correctly
5. **Document**: Update README with examples

## Testing

### Manual Testing Checklist

- [ ] App starts without errors
- [ ] Fetches trades from data source
- [ ] Stores trades in database
- [ ] Sends email notifications
- [ ] Handles configuration errors gracefully
- [ ] Docker container builds and runs
- [ ] Logs are informative and not too verbose

### Future: Automated Tests

We'd love to add automated testing! Consider contributing:
- Unit tests for individual functions
- Integration tests for the full workflow
- Mock data for testing without hitting real APIs

## Questions?

- Open an issue for questions
- Tag with `question` label
- Be respectful and patient

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow
- No harassment or discrimination

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

Thank you for helping make Congressional trading more transparent! 🏛️
