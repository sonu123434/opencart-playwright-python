from playwright.sync_api import Page, expect

from config import CART_PATH, build_url
from pages.base_page import BasePage


class CheckoutPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

    def expect_redirect_to_cart(self):
        expect(self.page).to_have_url(build_url(CART_PATH))
        expect(self.page.locator("#content")).to_contain_text("Shopping Cart")
        return self
