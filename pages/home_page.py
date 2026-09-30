from playwright.sync_api import Page

from config import HOME_PATH, build_url
from pages.base_page import BasePage


class HomePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.logo = self.page.locator("#logo")
        self.my_account_button = self.page.locator("#top-links li.dropdown > a")
        self.login_menu_link = self.page.locator(
            '#top-links .dropdown-menu a[href*="route=account/login"]'
        )

    def open(self):
        self.navigate(build_url(HOME_PATH))
        return self

    def click_my_account(self):
        self.my_account_button.first.click()
        return self

    def click_login_from_my_account(self):
        self.login_menu_link.click()
        return self

    def expect_loaded(self):
        self.logo.wait_for(state="visible")
        self.expect_title("Your Store")
