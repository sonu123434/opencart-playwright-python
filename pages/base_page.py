from pathlib import Path

from playwright.sync_api import Page, expect

from config import DEFAULT_TIMEOUT as DEFAULT_NAVIGATION_TIMEOUT


class BasePage:
    DEFAULT_TIMEOUT = DEFAULT_NAVIGATION_TIMEOUT

    def __init__(self, page: Page):
        self.page = page

    def navigate(self, url: str):
        self.page.goto(url, wait_until="domcontentloaded", timeout=self.DEFAULT_TIMEOUT)

    def get_title(self):
        return self.page.title()

    def expect_title(self, expected_title: str):
        expect(self.page).to_have_title(expected_title)

    def wait_for_url_contains(self, text: str):
        expect(self.page).to_have_url(f"*{text}*")

    def take_screenshot(self, name: str):
        screenshot_dir = Path("artifacts")
        screenshot_dir.mkdir(exist_ok=True)
        self.page.screenshot(path=screenshot_dir / f"{name}.png", full_page=True)
        return screenshot_dir / f"{name}.png"
