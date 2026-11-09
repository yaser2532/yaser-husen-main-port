import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        page = await b.new_page(viewport={'width': 1440, 'height': 900})
        await page.goto('http://localhost:8080/')
        await page.wait_for_timeout(500)
        await page.mouse.move(720, 450)
        await page.wait_for_timeout(300)
        ss_path = "C:/Users/yhuse/.gemini/antigravity/brain/fc793577-a505-4be3-babf-536dd24e6ccd/clean_dot_elements.png"
        await page.screenshot(path=ss_path)
        print("Captured clean dot elements:", ss_path)
        await b.close()

if __name__ == '__main__':
    asyncio.run(main())
