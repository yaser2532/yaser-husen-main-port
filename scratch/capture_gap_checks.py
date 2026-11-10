import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        for w, h, name in [(375, 812, 'mobile_375'), (414, 896, 'mobile_414'), (768, 1024, 'tablet_768'), (1440, 900, 'desktop_1440')]:
            page = await browser.new_page(viewport={'width': w, 'height': h})
            await page.goto('http://localhost:8080/', wait_until='domcontentloaded')
            await asyncio.sleep(1.0)
            
            # Screenshot top
            await page.screenshot(path=f'scratch/gap_check_{name}_top.png')

            # Scroll to projects
            await page.evaluate('document.querySelector("#projects").scrollIntoView()')
            await asyncio.sleep(0.5)
            await page.screenshot(path=f'scratch/gap_check_{name}_projects.png')

            # Scroll to secret-desk
            await page.evaluate('document.querySelector("#secret-desk").scrollIntoView()')
            await asyncio.sleep(0.5)
            await page.screenshot(path=f'scratch/gap_check_{name}_desk.png')

            # Scroll to contact
            await page.evaluate('document.querySelector("#contact").scrollIntoView()')
            await asyncio.sleep(0.5)
            await page.screenshot(path=f'scratch/gap_check_{name}_contact.png')

            await page.close()

        await browser.close()
        print("Screenshots captured!")

if __name__ == '__main__':
    asyncio.run(main())
