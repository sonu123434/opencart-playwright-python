import pytest

from config import BASE_URL
from pages.home_page import HomePage
from pages.login_page import LoginPage


@pytest.fixture(scope="session")
def base_url():
    return BASE_URL


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
