import json

import pytest
from playwright.sync_api import sync_playwright




# 初始化浏览器
@pytest.fixture(scope="module")
def browser_fixture():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=1000)
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://app.dev.connectly.ai/flow")
        yield page, context
        browser.close()


# loginpage用例
def test_login(browser_fixture):
    page, context = browser_fixture
    # 输入用户名
    page.fill("//input[@id='1-email']", "test@connectly.ai")
    # 输入密码
    page.fill("//input[@name='password']", "test2024@cnt")
    # 点击LOG IN
    page.click("//button[@name='submit']")
    # 断言:出现首页元素
    page.wait_for_selector("//*[text()='Get Started']")
    assert page.locator("//*[text()='Get Started']").count() != 0


# test_resend用例
def test_resend(browser_fixture):
    page, context = browser_fixture
    # 选择重新发送&编辑
    page.click("//*[text()='Resend or edit a campaign']")
    page.wait_for_selector("//button[text()='Edit']")
    # 输入框输入Cnct Load Testing For Interview
    page.fill("//input[@id=':r0:']", "Cnct Load Testing For Interview")
    # 选择Cnct Load Testing For Interview
    page.keyboard.press("ArrowUp")
    page.keyboard.press("Enter")
    # 点击RESEND
    page.click("//button[text()='Resend']")
    page.wait_for_selector("//*[text()='All messages are approved!']")
    # 断言:出现All messages are approved!弹窗
    assert page.locator("//*[text()='All messages are approved!']").count() != 0



# Continue
def test_continue(browser_fixture):
    page, context = browser_fixture
    # 等待continue出现后,点击
    page.wait_for_selector("//button[text()='Continue']")
    page.click("//button[text()='Continue']")
    # 点击next
    page.wait_for_selector("//button[text()='Next']").is_enabled()
    page.click("//button[text()='Next']")
    # 点击Add recipient list
    page.wait_for_selector("//a[text()='Add recipient list']")
    assert page.locator("//a[text()='Add recipient list']").is_enabled()
    page.click("//a[text()='Add recipient list']")
    page.wait_for_timeout(5000)
    pages = context.pages
    # 切换标签页2
    page2 = pages[1]
    # 输入联系号码
    page2.keyboard.press("ArrowDown")
    page2.keyboard.type("086123456789")
    # 保存
    page2.keyboard.press("Control+s")
    page2.close()


    # 验证
    page.click("//button[text()='Verify']")
    page.wait_for_selector("//div[text()='Spreadsheet verified successfully']")
    assert page.locator("//div[text()='Spreadsheet verified successfully']").count() != 0
    page.click("//button[text()='Next']")


# sendnow用例
def test_sendnow(browser_fixture):
    page, context = browser_fixture
    page.click("//div[text()='Send Now']")
    # submit
    page.click("//button[text()='Submit Campaign']")
    try:
        # 断言:Congrats弹窗
        assert page.locator("//*[text()='Congrats, your campaign has been sent!']").count() != 0
    except:
        print("timeout!")