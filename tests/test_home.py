import logging

import pytest

logger = logging.getLogger(__name__)


@pytest.mark.smoke
@pytest.mark.sanity
def test_open_opencart(home_page, api_request_context):
    response = api_request_context.get("index.php?route=common/home")
    assert response.ok, f"Home endpoint returned HTTP {response.status}."
    logger.info("event=home_api_verified status=%s", response.status)

    home_page.open()
    home_page.expect_loaded()
    logger.info("event=home_ui_verified title=%s", home_page.get_title())
