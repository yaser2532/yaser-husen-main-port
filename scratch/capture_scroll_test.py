from playwright.sync_api import sync_playwright

def capture_scrolls():
    with sync_playwright() as p:
        browser = p.chromium.launch(channel='msedge', headless=True)
        page = browser.new_page(viewport={'width': 1440, 'height': 900})
        page.route('**/*.mp4', lambda r: r.abort())
        page.route('**/*.mp3', lambda r: r.abort())
        page.goto('http://localhost:8080/', wait_until='domcontentloaded')
        page.wait_for_timeout(1000)

        # Capture Hero (scroll = 0)
        page.screenshot(path="scratch/check_scroll_0.png")

        # Scroll to 1000 (Expertise)
        page.evaluate("() => window.scrollTo(0, 1000)")
        page.wait_for_timeout(1000)
        page.screenshot(path="scratch/check_scroll_1000.png")

        # Scroll to 2500 (About / Projects)
        page.evaluate("() => window.scrollTo(0, 2500)")
        page.wait_for_timeout(1000)
        page.screenshot(path="scratch/check_scroll_2500.png")

        # Scroll to 5000 (Creative lab)
        page.evaluate("() => window.scrollTo(0, 5000)")
        page.wait_for_timeout(1000)
        page.screenshot(path="scratch/check_scroll_5000.png")

        browser.close()

if __name__ == '__main__':
    capture_scrolls()
