import asyncio
from playwright.async_api import async_playwright

async def inspect():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1440, 'height': 900})
        await page.goto('http://localhost:8080/', wait_until='networkidle')
        await page.wait_for_timeout(3500)
        
        y_el = await page.query_selector('.hero-3d-char')
        if y_el:
            await y_el.screenshot(path='scratch/zoom_y.png')
            print('Saved zoom_y.png')
            
        h1_el = await page.query_selector('.hero-title')
        if h1_el:
            await h1_el.screenshot(path='scratch/zoom_title.png')
            print('Saved zoom_title.png')
            
        await browser.close()

if __name__ == '__main__':
    asyncio.run(inspect())
