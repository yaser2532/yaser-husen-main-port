import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1440, 'height': 900})
        await page.goto('http://localhost:8080/', wait_until='domcontentloaded')
        await asyncio.sleep(1.0)

        selectors = [
            ('.hero-actions .cta-button', 'Hero Button'),
            ('.project-filters .filter-btn', 'Filter Button'),
            ('.dock-btn', 'Dock Button'),
            ('.nav-resume-btn', 'Nav Resume Button'),
            ('#submit-btn', 'Submit Button')
        ]

        for sel, name in selectors:
            loc = page.locator(sel).first
            await loc.scroll_into_view_if_needed()
            await asyncio.sleep(0.3)
            # Use mouse move directly to element center
            box = await loc.bounding_box()
            await page.mouse.move(box['x'] + box['width']/2, box['y'] + box['height']/2)
            await asyncio.sleep(0.4)

            res = await loc.evaluate('''(el) => {
                const comp = window.getComputedStyle(el);
                return {
                    bgImage: comp.backgroundImage,
                    anim: comp.animationName,
                    color: comp.color
                };
            }''')
            print(f"[{name}] Hover State:", res)

        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
