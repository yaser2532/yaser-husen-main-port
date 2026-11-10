import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1440, 'height': 900})
        await page.goto('http://localhost:8080/', wait_until='domcontentloaded')
        await asyncio.sleep(1.0)

        btn = page.locator('.filter-btn').first
        await page.evaluate('''() => {
            const el = document.querySelector(".filter-btn");
            if (el) el.scrollIntoView({ block: "center", behavior: "instant" });
        }''')
        await asyncio.sleep(0.3)
        await btn.hover()
        await asyncio.sleep(0.3)

        info = await btn.evaluate('''(el) => {
            const comp = window.getComputedStyle(el);
            return {
                bg: comp.backgroundImage,
                bgColor: comp.backgroundColor,
                anim: comp.animationName,
                classes: el.className
            };
        }''')
        print("Filter button hover info:", info)
        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
