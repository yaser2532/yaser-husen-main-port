import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1440, 'height': 900})

        await page.goto("http://localhost:8080/", wait_until='networkidle')
        await page.wait_for_timeout(600)

        seam_check = await page.evaluate('''() => {
            const seam = document.querySelector('.hero-transition-seam');
            if (!seam) return { exists: false };
            const r = seam.getBoundingClientRect();
            const cs = window.getComputedStyle(seam);
            return {
                exists: true,
                rect: { top: r.top, bottom: r.bottom, height: r.height, width: r.width },
                display: cs.display,
                visibility: cs.visibility,
                opacity: cs.opacity,
                zIndex: cs.zIndex,
                background: cs.background,
                backdropFilter: cs.backdropFilter || cs.webkitBackdropFilter
            };
        }''')
        print("Seam check:", seam_check)
        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
