import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1440, 'height': 900})
        await page.goto('http://localhost:8080/', wait_until='domcontentloaded')
        await asyncio.sleep(1.0)

        btn = page.locator('#submit-btn')
        await btn.scroll_into_view_if_needed()
        await asyncio.sleep(0.5)

        info = await btn.evaluate('''(el) => {
            const rect = el.getBoundingClientRect();
            const elAtPoint = document.elementFromPoint(rect.left + rect.width/2, rect.top + rect.height/2);
            return {
                rect: { top: rect.top, bottom: rect.bottom, left: rect.left, right: rect.right },
                elAtPoint: elAtPoint ? { tag: elAtPoint.tagName, cls: elAtPoint.className, id: elAtPoint.id } : null
            };
        }''')
        print("Submit button info:", info)
        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
