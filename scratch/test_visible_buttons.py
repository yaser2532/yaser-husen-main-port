from playwright.sync_api import sync_playwright

def test_visible_buttons():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': 1440, 'height': 900})
        page.goto('http://localhost:8080/', wait_until='domcontentloaded')
        page.wait_for_timeout(300)
        
        button_selectors = [
            ('.hero-actions a.cta-button', 'Hero CTA Explore Button'),
            ('.nav-resume-btn', 'Navbar Resume Button'),
            ('#secret-message-btn', 'Secret Desk Message Button'),
            ('#footer-resume-btn', 'Footer Dock Resume Button'),
            ('.dock-btn', 'Dock Button')
        ]
        
        for sel, label in button_selectors:
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
                print(f"=== {label} ({sel}) ===")
                print(f"  textShadow: {st['textShadow']}")
                print(f"  boxShadow: {st['boxShadow']}")
                print(f"  color: {st['color']}")
                print(f"  border: {st['border']}")
        browser.close()

if __name__ == '__main__':
    test_visible_buttons()
