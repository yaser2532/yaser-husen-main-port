from playwright.sync_api import sync_playwright

def test_buttons():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': 1440, 'height': 900})
        page.goto('http://localhost:8080/')
        page.wait_for_timeout(300)
        
        selectors = ['.hero-actions a.cta-button', '.nav-resume-btn', '.dock-btn', '#submit-btn']
        for sel in selectors:
            btn = page.locator(sel).first
            if btn.count() > 0:
                btn.scroll_into_view_if_needed()
                btn.hover()
                page.wait_for_timeout(150)
                st = btn.evaluate('''el => {
                    const s = window.getComputedStyle(el);
                    return {
                        textShadow: s.textShadow,
                        boxShadow: s.boxShadow,
                        color: s.color,
                        border: s.borderColor
                    };
                }''')
                print(f"=== {sel} ===")
                print(f"  textShadow: {st['textShadow']}")
                print(f"  boxShadow: {st['boxShadow']}")
                print(f"  color: {st['color']}")
                print(f"  border: {st['border']}")
        browser.close()

if __name__ == '__main__':
    test_buttons()
