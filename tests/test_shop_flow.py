import logging

import pytest

logger = logging.getLogger(__name__)


@pytest.mark.regression
@pytest.mark.shopping
@pytest.mark.checkout
def test_opencart_full_flow(authenticated_account, product_page, cart_page, test_data):
    cart_page.open()
    cart_page.clear_cart()
    product_page.open_desktop_category()
    product_page.open_mac_category()
    product_page.open_imac_product()
    product_page.expect_product_page_loaded(test_data["product"]["name"])
    logger.info("event=product_selected name=%s", test_data["product"]["name"])

    product = test_data["product"]
    product_page.set_quantity(product["quantity"]).add_to_cart()
    product_page.expect_cart_summary(product["cart_summary"])
    logger.info(
        "event=product_added_to_cart name=%s quantity=%s",
        product["name"],
        product["quantity"],
    )
    cart_page.open()

    cart_page.expect_product_in_cart(product["name"], product["quantity"])
    cart_page.expect_totals(product["totals"])
    logger.info("event=cart_values_verified item=%s", product["name"])

    logger.info("event=checkout_started")
    checkout_page = cart_page.click_checkout()
    checkout_page.expect_redirect_to_cart()
