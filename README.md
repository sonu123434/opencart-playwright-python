<<<<<<< HEAD
# opencart-playwright-python
Playwright automation framework for OpenCart UI testing using Python and pytest
=======
# OpenCart Playwright Automation

This project is a simple Python-based UI automation suite built with `pytest` and `playwright`.

## Structure

- `config.py` - shared environment and URL configuration
- `pages/` - page object classes
- `tests/` - pytest test files and fixtures
- `artifacts/` - screenshots generated during test runs

## Run tests

```bash
pytest -q
```

## Common pattern

- Keep page selectors and interactions inside page objects
- Keep test assertions in the test files
- Reuse a base page class for shared behavior
- Store URL values in a single config file
>>>>>>> 179b709 (Initial commit)
