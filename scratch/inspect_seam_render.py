import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1440, 'height': 900})

        await page.goto("http://localhost:8080/", wait_until='networkidle')
        await page.wait_for_timeout(800)

        # Inspect computed backgrounds of body, html, header, overlay, seam, main, profile-expertise, cosmic-bg-container
        info = await page.evaluate('''() => {
            function getElemInfo(sel) {
                const el = document.querySelector(sel);
                if (!el) return null;
                const rect = el.getBoundingClientRect();
                const style = window.getComputedStyle(el);
                return {
                    selector: sel,
                    rect: { top: rect.top, bottom: rect.bottom, height: rect.height },
                    background: style.background,
                    backgroundColor: style.backgroundColor,
                    backgroundImage: style.backgroundImage,
                    borderBottom: style.borderBottom,
                    borderTop: style.borderTop,
                    boxShadow: style.boxShadow,
                    zIndex: style.zIndex,
                    opacity: style.opacity,
                    filter: style.filter,
                    backdropFilter: style.backdropFilter || style.webkitBackdropFilter
                };
            }
            return {
                scrollY: window.scrollY,
                windowH: window.innerHeight,
                elements: [
                    getElemInfo('header#home'),
                    getElemInfo('header#home::before'),
                    getElemInfo('.overlay'),
                    getElemInfo('.hero-transition-seam'),
                    getElemInfo('main.page-body-content'),
                    getElemInfo('#profile-expertise'),
                    getElemInfo('#profile-expertise::before'),
                    getElemInfo('#cosmic-bg-container'),
                    getElemInfo('#cosmic-canvas')
                ]
            };
        }''')
        
        print("=== Computed Styles & Rects ===")
        for el in info['elements']:
            if el:
                print(f"[{el['selector']}] height={el['rect']['height']}, top={el['rect']['top']}, bottom={el['rect']['bottom']}")
                print(f"   bg-color: {el['backgroundColor']}")
                print(f"   bg-image: {el['backgroundImage'][:80] if el['backgroundImage'] else 'none'}")
                print(f"   border-top: {el['borderTop']}, border-bottom: {el['borderBottom']}")
                print(f"   z-index: {el['zIndex']}")

        # Take screenshot of the seam at scroll=0, scroll=300, scroll=600
        for sy in [0, 250, 500, 750]:
            await page.evaluate(f"window.scrollTo(0, {sy})")
            await page.wait_for_timeout(300)
            ss_path = f"C:/Users/yhuse/.gemini/antigravity/brain/fc793577-a505-4be3-babf-536dd24e6ccd/inspect_seam_scroll_{sy}.png"
            await page.screenshot(path=ss_path, full_page=False)
            print(f"Captured screenshot at scroll={sy}: {ss_path}")

        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
