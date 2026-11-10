from playwright.sync_api import sync_playwright

def test_dock_and_secret():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': 1440, 'height': 900})
        page.goto('http://localhost:8080/')
        page.wait_for_timeout(300)
        
        # Test footer dock resume button
        btn = page.locator('#footer-resume-btn').first
        btn.hover(force=True)
        page.wait_for_timeout(150)
        st = btn.evaluate('''el => {
            const s = window.getComputedStyle(el);
            return {
                textShadow: s.textShadow,
                boxShadow: s.boxShadow,
                color: s.color,
                bg: s.backgroundImage || s.background
            };
        }''')
        print("=== Footer Resume Button ===")
        print(f"  textShadow: {st['textShadow']}")
        print(f"  boxShadow: {st['boxShadow']}")
        print(f"  color: {st['color']}")
        page.screenshot(path='scratch/footer_resume_btn_hover.png')
        
        # Test secret message button with force=True
        sec_btn = page.locator('#secret-message-btn').first
        sec_btn.hover(force=True)
        page.wait_for_timeout(150)
        sec_st = sec_btn.evaluate('''el => {
            const s = window.getComputedStyle(el);
            return {
                textShadow: s.textShadow,
                boxShadow: s.boxShadow,
                color: s.color,
                bg: s.backgroundImage || s.background
            };
        }''')
        print("=== Secret Desk Button ===")
        print(f"  textShadow: {sec_st['textShadow']}")
        print(f"  boxShadow: {sec_st['boxShadow']}")
        print(f"  color: {sec_st['color']}")
        page.screenshot(path='scratch/secret_btn_hover.png')

        browser.close()

if __name__ == '__main__':
    test_dock_and_secret()
