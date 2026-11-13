from playwright.sync_api import sync_playwright

def test_todo_e2e():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("http://127.0.0.1:5000")

        page.fill("#title", "測試待辦")
        page.click("button:has-text('新增')")
        page.wait_for_timeout(500)

        assert page.is_visible("text=測試待辦")

        page.click("button:has-text('完成')")
        page.wait_for_timeout(500)

        assert page.locator("li.done").count() == 1

        page.click("button:has-text('刪除')")
        page.wait_for_timeout(500)

        browser.close()