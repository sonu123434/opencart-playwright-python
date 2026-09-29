from playwright.sync_api import Page, expect

from pages.account_page import AccountPage
from pages.home_page import HomePage
from pages.login_page import LoginPage


def test_login_page(page: Page):
    home_page = HomePage(page)
    login_page = LoginPage(page)

    home_page.open()
    home_page.click_my_account()
    home_page.click_login_from_my_account()

    expect(page).to_have_url("https://naveenautomationlabs.com/opencart/index.php?route=account/login")
    login_page.verify_returning_customer_section()

    login_page.enter_email("test.automation.opencart@gmail.com")
    login_page.enter_password("Test@12345")
    login_page.click_login()

    account_page = AccountPage(page)
    account_page.expect_logged_in()
    expect(page).to_have_url("https://naveenautomationlabs.com/opencart/index.php?route=account/account")