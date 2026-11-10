import sys
from playwright.sync_api import sync_playwright

def inspect_sections():
    with sync_playwright() as p:
        browser = p.chromium.launch(channel='msedge', headless=True)
        page = browser.new_page(viewport={'width': 1440, 'height': 900})

        page.route('**/*.mp4', lambda r: r.abort())
        page.route('**/*.mp3', lambda r: r.abort())

        page.goto('http://localhost:8080/', wait_until='domcontentloaded')
        page.wait_for_timeout(1000)

        sections_info = page.evaluate("""() => {
            const list = [];
            const all = document.querySelectorAll('header, section, footer, main, div.container');
            all.forEach(el => {
                const cs = window.getComputedStyle(el);
                if (cs.backgroundColor !== 'rgba(0, 0, 0, 0)' || cs.backgroundImage !== 'none') {
                    list.push({
                        tag: el.tagName,
                        id: el.id,
                        className: el.className,
                        bg: cs.backgroundColor,
                        bgImage: cs.backgroundImage ? cs.backgroundImage.slice(0, 60) : 'none',
                        opacity: cs.opacity,
                        zIndex: cs.zIndex
                    });
                }
            });
            return list;
        }""")
        print("--- Elements with non-transparent backgrounds ---")
        for item in sections_info:
            print(item)

        browser.close()

if __name__ == '__main__':
    inspect_sections()
