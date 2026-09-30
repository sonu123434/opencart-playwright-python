# OpenCart Playwright Automation

Python UI automation using pytest and Playwright, organized with page objects and reusable pytest fixtures.

## Setup

Use Python 3.13 and PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m playwright install chromium
```

Install Firefox and WebKit as well to run the full browser matrix:

```powershell
python -m playwright install firefox webkit
```

## Configuration

Copy the safe example to a local, Git-ignored file:

```powershell
Copy-Item credentials.example.json credentials.json
notepad credentials.json
```

The file has URL profiles for `qa`, `uat`, `staging`, and `production`. Fill in each environment URL you intend to use. QA is selected by default; selecting an environment without a URL fails instead of silently targeting QA. Credentials can be set at the file root or per environment. The example's email and password are blank placeholders.

Environment variables override local settings:

```powershell
$env:OPENCART_ENV = "qa"
$env:OPENCART_BASE_URL = "https://your-qa-site.example/opencart/"
$env:OPENCART_TEST_EMAIL = "your-test-account@example.com"
$env:OPENCART_TEST_PASSWORD = "your-test-password"
```

`OPENCART_CREDENTIALS_FILE` can point to another settings JSON file. Relative paths are resolved from the current directory. Never commit `credentials.json` or put real credentials in `credentials.example.json`. Previously hard-coded credentials exist in Git history; rotate them if still active.

## Running Tests

Run the default Chromium suite with an HTML report:

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

Show the browser while tests run:

```powershell
.\.venv\Scripts\python.exe -m pytest --headed -q
```

Run one or more browsers:

```powershell
.\.venv\Scripts\python.exe -m pytest --browser chromium --browser firefox --browser webkit -q
```

Run selected categories:

```powershell
.\.venv\Scripts\python.exe -m pytest -m smoke
.\.venv\Scripts\python.exe -m pytest -m "login or shopping"
```

Pytest is configured for two parallel workers and one retry only for recognized network transport errors. Timeouts and assertion failures are not retried. The report is written to `artifacts/report.html`; failure screenshots and Playwright traces are saved under `artifacts/`. Open a trace with:

```powershell
.\.venv\Scripts\python.exe -m playwright show-trace artifacts\<test-name>-trace.zip
```

Retries are restricted to browser/network transport errors (`net::ERR_`, `ECONNRESET`, and `NS_ERROR_NET_`); timeouts and assertion failures are not retried.

## Project Layout

- `config.py` - environment selection, settings loading, routes, and URL building
- `credentials.example.json` - safe template for local settings
- `pages/` - page objects, including checkout boundary behavior
- `tests/conftest.py` - browser, page, API, credentials, logging, and failure-artifact fixtures/hooks
- `tests/data/test_data.json` - non-secret input and expected product/login data
- `tests/` - smoke, regression, negative, configuration, and UI/API tests
- `.github/workflows/tests.yml` - CI browser matrix and artifact upload
- `artifacts/` - generated HTML report, screenshots, and traces; ignored by Git

## Quality and CI

Run lint and formatting checks locally:

```powershell
.\.venv\Scripts\ruff.exe check .
.\.venv\Scripts\ruff.exe format --check .
```

GitHub Actions runs Chromium, Firefox, and WebKit jobs. Configure GitHub environments named `qa`, `uat`, `staging`, and `production`; set `OPENCART_BASE_URL` as an environment variable and `OPENCART_TEST_EMAIL` / `OPENCART_TEST_PASSWORD` as secrets. The workflow can be manually dispatched against one of those environments. Without credentials, authenticated tests skip.

## Contributing

- Keep selectors and browser interactions in page objects; keep scenario assertions in tests.
- Put non-secret inputs and expectations in `tests/data/test_data.json`.
- Add a pytest marker to each new test and document new markers in `pytest.ini`.
- Never commit real account credentials or generated artifacts.
- Run `ruff check .`, `ruff format --check .`, and the relevant pytest tests before opening a pull request.

## Scope and Troubleshooting

The current demo site redirects checkout back to the cart. `CheckoutPage` verifies that observed boundary; it does not claim a completed checkout. Checkout field validation needs an environment where the checkout page is reachable. The demo product also has no client-side minimum quantity validation; the negative quantity test checks that quantity zero does not add a cart item. API request support is available as a fixture, but no API seed/cleanup flow is configured because no supported store API endpoint has been verified.

- If authenticated tests skip, configure both email and password through environment variables or `credentials.json`.
- If a non-QA environment fails with a missing URL, configure its profile or `OPENCART_BASE_URL`.
- If a browser executable is missing, install it with `python -m playwright install <browser>`.
- Check `artifacts/report.html`, the failure screenshot, and the trace zip for test failure details.
