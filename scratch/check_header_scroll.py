import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1440, 'height': 900})
        await page.goto('http://localhost:8080/', wait_until='domcontentloaded')
        await asyncio.sleep(1.0)

        # Scroll to #submit-btn
        await page.locator('#submit-btn').scroll_into_view_if_needed()
        await asyncio.sleep(0.5)

        info = await page.evaluate('''() => {
            const btn = document.querySelector("#submit-btn");
            const btnRect = btn.getBoundingClientRect();
            const elAtPoint = document.elementFromPoint(btnRect.left + btnRect.width/2, btnRect.top + btnRect.height/2);
            const header = document.querySelector("#home");
            const headerRect = header ? header.getBoundingClientRect() : null;
            return {
                btnRect: { top: btnRect.top, bottom: btnRect.bottom, left: btnRect.left, right: btnRect.right },
                headerRect: headerRect,
                elAtPoint: elAtPoint ? { tag: elAtPoint.tagName, cls: elAtPoint.className, text: elAtPoint.textContent.slice(0, 30) } : null
            };
        }''')
        print("Header scroll check:", info)
        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
