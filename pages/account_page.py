from playwright.sync_api import Page, expect

from pages.base_page import BasePage


class AccountPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.account_heading = self.page.locator("#content").get_by_role(
            "heading", name="My Account"
        )
        self.edit_account_info = self.page.get_by_text("Edit your account information")

    def expect_logged_in(self):
        expect(self.account_heading).to_be_visible()
        expect(self.edit_account_info).to_be_visible()
        return self
