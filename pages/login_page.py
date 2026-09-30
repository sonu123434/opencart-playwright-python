import re

from playwright.sync_api import Page, expect

from config import LOGIN_PATH, build_url
from pages.base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.returning_customer_heading = self.page.get_by_role(
            "heading", name="Returning Customer"
        )
        self.email_input = self.page.locator("#input-email")
        self.password_input = self.page.locator("#input-password")
        self.submit_button = self.page.locator("input[type='submit']")
        self.alert_danger = self.page.locator(".alert-danger")

    def open(self):
        self.navigate(build_url(LOGIN_PATH))
        return self

    def verify_returning_customer_section(self):
        expect(self.returning_customer_heading).to_be_visible()
        return self

    def expect_login_error(self):
        expect(self.alert_danger).to_be_visible()
        expect(self.alert_danger).to_have_text(re.compile(r"\S+"))
        expect(self.page).to_have_url(build_url(LOGIN_PATH))
        return self

    def enter_email(self, email: str):
        self.email_input.fill(email)
        return self

    def enter_password(self, password: str):
        self.password_input.fill(password)
        return self

    def click_login(self):
        self.submit_button.click()
        return self

    def login_as(self, email: str, password: str):
        self.enter_email(email)
        self.enter_password(password)
        self.click_login()
        return self
