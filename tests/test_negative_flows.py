import logging

import pytest

logger = logging.getLogger(__name__)


@pytest.mark.regression
@pytest.mark.login
@pytest.mark.parametrize(
    "scenario", ["empty", "invalid"], ids=["empty-fields", "invalid-credentials"]
)
def test_login_rejects_invalid_credentials(login_page, test_data, scenario):
    login_page.open()
    login_page.login_as(**test_data["login"][scenario])
    login_page.expect_login_error()
    logger.info("event=login_rejected scenario=%s", scenario)


@pytest.mark.regression
@pytest.mark.login
def test_login_rejects_invalid_password(login_page, test_credentials, test_data):
    login_page.open()
    login_page.login_as(
        email=test_credentials["email"],
        password=test_data["login"]["invalid"]["password"],
    )
    login_page.expect_login_error()
    logger.info("event=login_rejected scenario=invalid_password")


@pytest.mark.regression
@pytest.mark.shopping
def test_zero_quantity_does_not_add_product(product_page, cart_page, test_data):
    product = test_data["product"]
    product_page.open_imac_directly()
    product_page.set_quantity(product["invalid_quantity"]).add_to_cart()
    cart_page.open()
    cart_page.expect_empty()
    logger.info("event=invalid_quantity_rejected quantity=%s", product["invalid_quantity"])
