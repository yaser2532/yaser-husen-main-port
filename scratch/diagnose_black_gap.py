from playwright.sync_api import sync_playwright

def test_viewports():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for width in [1920, 1440, 1200, 1024, 768, 375]:
            page = browser.new_page(viewport={'width': width, 'height': 900})
            page.goto('http://localhost:8080/', wait_until='domcontentloaded')
            page.wait_for_timeout(400)
            
            info = page.evaluate('''() => {
                const docWidth = document.documentElement.offsetWidth;
                const scrollWidth = document.documentElement.scrollWidth;
                const innerWidth = window.innerWidth;
                const bodyWidth = document.body.offsetWidth;
                
                const sections = Array.from(document.querySelectorAll('section, header, footer, main, nav, .hero-section, .cyber-dock-footer')).map(s => {
                    const rect = s.getBoundingClientRect();
                    return {
                        id: s.id || (s.className ? s.className.split(' ')[0] : s.tagName),
                        rectRight: rect.right,
                        rectWidth: rect.width,
                        rectLeft: rect.left
                    };
                });
                
                const overflowing = [];
                document.querySelectorAll('*').forEach(el => {
                    const r = el.getBoundingClientRect();
                    if (r.right > innerWidth + 1) {
                        overflowing.push({ tag: el.tagName, id: el.id, cls: String(el.className).substring(0, 30), right: r.right, width: r.width });
                    }
                });
                
                return { docWidth, scrollWidth, innerWidth, bodyWidth, sections, overflowing: overflowing.slice(0, 10) };
            }''')
            print(f"=== Viewport {width} ===")
            print(f"docWidth: {info['docWidth']}, scrollWidth: {info['scrollWidth']}, innerWidth: {info['innerWidth']}, bodyWidth: {info['bodyWidth']}")
            for s in info['sections']:
                if abs(s['rectRight'] - width) > 2 or s['rectLeft'] > 2:
                    print(f"  Gap/offset: {s['id']}: left={s['rectLeft']:.1f}, right={s['rectRight']:.1f}, width={s['rectWidth']:.1f} (diff={width - s['rectRight']:.1f}px)")
            if info['overflowing']:
                print(f"  Overflowing elements: {info['overflowing']}")
        browser.close()

if __name__ == '__main__':
    test_viewports()
