import sys
from playwright.sync_api import sync_playwright

def check():
    with sync_playwright() as p:
        browser = p.chromium.launch(channel='msedge', headless=True)
        page = browser.new_page(viewport={'width': 1440, 'height': 900})

        page.route('**/*.mp4', lambda r: r.abort())
        page.route('**/*.mp3', lambda r: r.abort())

        logs = []
        page.on('console', lambda m: logs.append(f"[{m.type}] {m.text}"))
        errs = []
        page.on('pageerror', lambda e: errs.append(str(e)))

        page.goto('http://localhost:8080/', wait_until='domcontentloaded')
        page.wait_for_timeout(1500)

        info = page.evaluate("""() => {
            const container = document.getElementById('cosmic-bg-container');
            const canvas = document.getElementById('cosmic-canvas');
            const header = document.querySelector('header');
            const main = document.querySelector('.page-body-content');
            return {
                threeDefined: typeof THREE !== 'undefined',
                containerExists: Boolean(container),
                containerStyle: container ? {
                    display: window.getComputedStyle(container).display,
                    opacity: window.getComputedStyle(container).opacity,
                    zIndex: window.getComputedStyle(container).zIndex,
                    position: window.getComputedStyle(container).position,
                    bgImage: window.getComputedStyle(container).backgroundImage.slice(0, 80)
                } : null,
                canvasSize: canvas ? { width: canvas.width, height: canvas.height } : null,
                headerStyle: header ? {
                    position: window.getComputedStyle(header).position,
                    zIndex: window.getComputedStyle(header).zIndex,
                    bgImage: window.getComputedStyle(header).backgroundImage.slice(0, 80),
                    bgAttachment: window.getComputedStyle(header).backgroundAttachment
                } : null,
                mainStyle: main ? {
                    position: window.getComputedStyle(main).position,
                    zIndex: window.getComputedStyle(main).zIndex,
                    bgColor: window.getComputedStyle(main).backgroundColor
                } : null
            };
        }""")
        print("DOM & CSS diagnostic:", info)
        print("Errors:", errs)
        print("Console logs count:", len(logs))
        for l in logs[:15]:
            print(l)
        browser.close()

if __name__ == '__main__':
    check()
