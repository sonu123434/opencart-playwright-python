import base64
import json
import logging
import os
import re
from pathlib import Path

import pytest
from pytest_html import extras

from config import (
    get_base_url,
    get_environment_settings,
    load_local_settings,
    local_settings_path,
)
from pages.account_page import AccountPage
from pages.cart_page import CartPage
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.product_page import ProductPage

logger = logging.getLogger(__name__)


def pytest_configure(config):
    Path("artifacts").mkdir(exist_ok=True)


def pytest_html_report_title(report):
    report.title = "OpenCart Playwright Test Report"


def pytest_runtest_setup(item):
    logger.info("event=test_started test=%s", item.nodeid)


def _artifact_basename(nodeid):
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", nodeid).strip("_")[:180]


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_call(item):
    page = item.funcargs.get("page")
    tracing_started = False
    if page is not None:
        try:
            page.context.tracing.start(screenshots=True, snapshots=True, sources=True)
            tracing_started = True
        except Exception:
            logger.exception("event=trace_start_failed test=%s", item.nodeid)

    outcome = yield
    if tracing_started:
        if outcome.excinfo is not None:
            trace_path = Path("artifacts") / f"{_artifact_basename(item.nodeid)}-trace.zip"
            try:
                page.context.tracing.stop(path=str(trace_path))
                item._playwright_trace_path = trace_path
            except Exception:
                logger.exception("event=trace_save_failed test=%s", item.nodeid)
        else:
            page.context.tracing.stop()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)

    if report.when == "call" and not report.failed:
        logger.info(
            "event=test_finished test=%s outcome=passed duration_seconds=%.3f",
            item.nodeid,
            report.duration,
        )
        return
    if not report.failed:
        return

    artifact_dir = Path("artifacts")
    artifact_dir.mkdir(exist_ok=True)
    report_extras = list(getattr(report, "extras", []))
    page = item.funcargs.get("page")
    if page is not None and not page.is_closed():
        screenshot_path = artifact_dir / f"{_artifact_basename(item.nodeid)}-failure.png"
        try:
            page.screenshot(path=str(screenshot_path), full_page=True)
            screenshot_data = base64.b64encode(screenshot_path.read_bytes()).decode("ascii")
            report_extras.append(extras.png(screenshot_data, name="Failure screenshot"))
            logger.error("event=failure_screenshot path=%s", screenshot_path)
        except Exception:
            logger.exception("event=failure_screenshot_failed test=%s", item.nodeid)

    trace_path = getattr(item, "_playwright_trace_path", None)
    if trace_path is not None:
        report_extras.append(extras.url(trace_path.name, name="Playwright trace"))

    report.extras = report_extras
    logger.error(
        "event=test_failed test=%s phase=%s duration_seconds=%.3f",
        item.nodeid,
        report.when,
        report.duration,
    )


@pytest.fixture(scope="session")
def base_url():
    return get_base_url()


@pytest.fixture(scope="session")
def browser_context_args():
    return {
        "viewport": {"width": 1440, "height": 980},
        "screen": {"width": 1440, "height": 980},
    }


@pytest.fixture
def home_page(page):
    return HomePage(page)


@pytest.fixture
def login_page(page):
    return LoginPage(page)


@pytest.fixture
def account_page(page):
    return AccountPage(page)


@pytest.fixture
def product_page(page):
    return ProductPage(page)


@pytest.fixture
def cart_page(page):
    return CartPage(page)


@pytest.fixture(scope="session")
def test_data():
    data_path = Path(__file__).parent / "data" / "test_data.json"
    try:
        data = json.loads(data_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        pytest.fail(f"Could not load test data from {data_path}: {error}", pytrace=False)
    if not isinstance(data, dict):
        pytest.fail("Test data must contain a JSON object.", pytrace=False)
    return data


@pytest.fixture
def test_credentials():
    email = os.getenv("OPENCART_TEST_EMAIL")
    password = os.getenv("OPENCART_TEST_PASSWORD")
    environment_credentials_configured = email is not None or password is not None
    if environment_credentials_configured and (not email or not password):
        pytest.fail(
            "Set both OPENCART_TEST_EMAIL and OPENCART_TEST_PASSWORD to non-empty values.",
            pytrace=False,
        )

    configured_path = os.getenv("OPENCART_CREDENTIALS_FILE")
    credentials_path = local_settings_path()
    if environment_credentials_configured:
        settings = {}
        profile = {}
    else:
        try:
            settings = load_local_settings()
            profile = get_environment_settings(settings)
        except (OSError, ValueError) as error:
            pytest.fail(
                f"Could not load credentials for the configured environment: {error}",
                pytrace=False,
            )

    if email is None:
        email = profile.get("email", settings.get("email"))
    if password is None:
        password = profile.get("password", settings.get("password"))

    if not email and not password:
        if configured_path and not credentials_path.is_file():
            pytest.fail(
                f"Credential file does not exist: {credentials_path}",
                pytrace=False,
            )
        pytest.skip(
            "Set OPENCART_TEST_EMAIL and OPENCART_TEST_PASSWORD, "
            "or provide credentials in the selected environment profile."
        )

    if not isinstance(email, str) or not email.strip():
        pytest.fail("A non-empty test email is required.", pytrace=False)
    if not isinstance(password, str) or not password:
        pytest.fail("A non-empty test password is required.", pytrace=False)

    return {"email": email.strip(), "password": password}


@pytest.fixture
def api_request_context(playwright, base_url):
    request_context = playwright.request.new_context(base_url=base_url)
    yield request_context
    request_context.dispose()


@pytest.fixture
def login_form(home_page, login_page):
    home_page.open()
    home_page.click_my_account()
    home_page.click_login_from_my_account()
    return login_page


@pytest.fixture
def authenticated_account(login_form, account_page, test_credentials):
    login_form.login_as(**test_credentials)
    account_page.expect_logged_in()
    return account_page
