import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1920, 'height': 1080})
        await page.goto('http://localhost:8080/', wait_until='domcontentloaded')
        await asyncio.sleep(0.5)

        info = await page.evaluate('''() => {
            const el = document.querySelector("#about-me");
            const comp = window.getComputedStyle(el);
            return {
                transform: comp.transform,
                rawTransform: el.style.transform,
                classes: el.className,
                filter: comp.filter
            };
        }''')
        print("About me transform:", info)
        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
