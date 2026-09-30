from playwright.sync_api import Page, expect

from config import DESKTOP_CATEGORY_PATH, IMAC_PRODUCT_PATH, MAC_CATEGORY_PATH, build_url
from pages.base_page import BasePage


class ProductPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.desktop_menu = self.page.locator(f'#menu a[href*="{DESKTOP_CATEGORY_PATH}"]').first
        self.show_all_desktops_link = self.page.get_by_role("link", name="Show All Desktops")
        self.mac_submenu = self.page.locator(f'#menu a[href*="{MAC_CATEGORY_PATH}"]')
        self.imac_product_link = (
            self.page.locator(f'a[href*="{IMAC_PRODUCT_PATH}"]').filter(has_text="iMac").first
        )
        self.add_to_cart_button = self.page.locator("#button-cart")
        self.quantity_input = self.page.locator("#input-quantity")
        self.cart_icon = self.page.locator("#cart")
        self.view_cart_link = self.page.get_by_role("link", name="View Cart")

    def open_desktop_category(self):
        self.desktop_menu.hover()
        self.show_all_desktops_link.click()
        expect(self.page).to_have_url(build_url(DESKTOP_CATEGORY_PATH))
        return self

    def open_mac_category(self):
        self.desktop_menu.hover()
        self.mac_submenu.click()
        expect(self.page).to_have_url(build_url(MAC_CATEGORY_PATH))
        return self

    def open_imac_product(self):
        self.imac_product_link.wait_for(state="visible", timeout=30000)
        self.imac_product_link.click()
        return self

    def add_to_cart(self):
        with self.page.expect_response(
            lambda response: "route=checkout/cart/add" in response.url
        ) as response_info:
            self.add_to_cart_button.click()
        response = response_info.value
        assert response.ok, f"Add-to-cart request failed with HTTP {response.status}."
        return self

    def open_imac_directly(self):
        self.navigate(build_url(IMAC_PRODUCT_PATH))
        return self

    def expect_cart_summary(self, summary: str):
        expect(self.cart_icon).to_contain_text(summary)
        return self

    def set_quantity(self, quantity: str):
        self.quantity_input.fill(quantity)
        return self

    def open_cart(self):
        self.cart_icon.click()
        self.view_cart_link.click()
        return self

    def expect_product_page_loaded(self, product_name: str):
        expect(self.page).to_have_url(build_url(IMAC_PRODUCT_PATH))
        expect(self.page.locator("h1")).to_contain_text(product_name)
        return self
