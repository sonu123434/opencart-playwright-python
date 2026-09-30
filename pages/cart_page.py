from playwright.sync_api import Page, expect

from config import CART_PATH, build_url
from pages.base_page import BasePage
from pages.checkout_page import CheckoutPage


class CartPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.remove_buttons = self.page.locator('button[data-original-title="Remove"]')
        self.checkout_link = self.page.locator("a[href*='route=checkout/checkout']").first

    def open(self):
        self.navigate(build_url(CART_PATH))
        return self

    def clear_cart(self):
        while self.remove_buttons.count() > 0:
            with self.page.expect_navigation(wait_until="domcontentloaded"):
                self.remove_buttons.first.click()
        return self

    def expect_totals(self, totals: list[dict[str, str]]):
        rows = self.page.locator("#content tr")
        for total in totals:
            row = rows.filter(has_text=total["label"])
            expect(row).to_be_visible()
            expect(row).to_contain_text(total["amount"])
        return self

    def expect_product_in_cart(self, product_name: str, quantity: str):
        product_row = self.page.locator("#content table tbody tr").filter(has_text=product_name)
        expect(product_row).to_be_visible()
        expect(product_row.locator('input[type="text"]')).to_have_value(quantity)
        return self

    def expect_empty(self):
        expect(self.page.locator("#content")).to_contain_text("Your shopping cart is empty!")
        return self

    def click_checkout(self):
        self.checkout_link.click()
        return CheckoutPage(self.page)
