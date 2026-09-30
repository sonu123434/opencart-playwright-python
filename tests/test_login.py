import logging

import pytest
from playwright.sync_api import Page, expect

from config import ACCOUNT_PATH, LOGIN_PATH, build_url

logger = logging.getLogger(__name__)


@pytest.mark.smoke
@pytest.mark.login
def test_login_page(page: Page, login_form, account_page, test_credentials):
    expect(page).to_have_url(build_url(LOGIN_PATH))
    login_form.verify_returning_customer_section()
    login_form.login_as(**test_credentials)
    account_page.expect_logged_in()
    expect(page).to_have_url(build_url(ACCOUNT_PATH))
    logger.info("event=login_successful")
