import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1440, 'height': 900})
        await page.goto('http://localhost:8080/', wait_until='domcontentloaded')
        await asyncio.sleep(1.0)

        # Center #submit-btn
        await page.evaluate('''() => {
            const btn = document.querySelector("#submit-btn");
            btn.scrollIntoView({ block: "center", behavior: "instant" });
        }''')
        await asyncio.sleep(0.5)

        btn = page.locator('#submit-btn')
        await btn.hover()
        await asyncio.sleep(0.3)

        info = await btn.evaluate('''(el) => {
            const comp = window.getComputedStyle(el);
            const spanComp = window.getComputedStyle(el.querySelector('span'));
            return {
                bg: comp.backgroundImage,
                anim: comp.animationName,
                color: comp.color,
                spanColor: spanComp.color
            };
        }''')
        print("Submit button hover info:", info)
        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
