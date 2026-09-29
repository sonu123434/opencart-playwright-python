from playwright.sync_api import Page


def test_open_opencart(page: Page, home_page):
    home_page.open()
    home_page.expect_loaded()
    assert page.title() == "Your Store"