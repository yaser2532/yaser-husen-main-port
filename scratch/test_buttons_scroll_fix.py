import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1440, 'height': 900})
        await page.goto('http://localhost:8080/', wait_until='domcontentloaded')
        await asyncio.sleep(1.0)

        selectors = [
            ('.hero-actions .cta-button', 'Hero Explore Button'),
            ('.project-filters .filter-btn', 'Project Filter Button'),
            ('.dock-btn', 'Dock Button'),
            ('.nav-resume-btn', 'Nav Resume Button'),
        ]

        for sel, name in selectors:
            loc = page.locator(sel).first
            await page.evaluate(f'''() => {{
                const el = document.querySelector("{sel}");
                if (el) el.scrollIntoView({{ block: "center", behavior: "instant" }});
            }}''')
            await asyncio.sleep(0.3)
            await loc.hover()
            await asyncio.sleep(0.3)

            res = await loc.evaluate('''(el) => {
                const comp = window.getComputedStyle(el);
                return {
                    bgImage: comp.backgroundImage,
                    anim: comp.animationName,
                    color: comp.color
                };
            }''')
            print(f"[{name}] Hover:", res)

        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
