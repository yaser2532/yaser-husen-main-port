from playwright.sync_api import sync_playwright

def inspect_direct():
    with sync_playwright() as p:
        browser = p.chromium.launch(channel='msedge', headless=True)
        page = browser.new_page(viewport={'width': 1440, 'height': 900})
        page.route('**/*.mp4', lambda r: r.abort())
        page.route('**/*.mp3', lambda r: r.abort())
        page.goto('http://localhost:8080/', wait_until='domcontentloaded')
        page.wait_for_timeout(1000)

        res = page.evaluate("""() => {
            const ids = ['home', 'profile-expertise', 'about-me', 'projects', 'creative-lab', 'certificates', 'secret-desk', 'contact'];
            return ids.map(id => {
                const el = document.getElementById(id);
                if (!el) return { id, exists: false };
                const cs = window.getComputedStyle(el);
                const rect = el.getBoundingClientRect();
                return {
                    id,
                    exists: true,
                    top: rect.top,
                    height: rect.height,
                    bg: cs.backgroundColor,
                    bgImg: cs.backgroundImage,
                    zIndex: cs.zIndex,
                    opacity: cs.opacity
                };
            });
        }""")
        for r in res:
            print(r)
        browser.close()

if __name__ == '__main__':
    inspect_direct()
