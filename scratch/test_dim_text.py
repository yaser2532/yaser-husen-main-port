import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1440, 'height': 900})

        await page.goto("http://localhost:8080/", wait_until='networkidle')
        await page.wait_for_timeout(500)

        h1_el = await page.query_selector('.hero-title')
        box = await h1_el.bounding_box()
        x = box['x'] + 50
        y = box['y'] + box['height'] / 2
        print(f"Testing over text at x={x}, y={y}")

        el_info = await page.evaluate('''(pt) => {
            const el = document.elementFromPoint(pt.x, pt.y);
            return {
                tag: el ? el.tagName : null,
                classes: el ? el.className : null,
                outer: el ? el.outerHTML.substring(0, 100) : null
            };
        }''', {'x': x, 'y': y})
        print("elementFromPoint:", el_info)

        # Move mouse and wait
        await page.mouse.move(x, y)
        await page.wait_for_timeout(400)

        drone_info = await page.evaluate('''() => {
            const ds = window.drones.getDrones();
            return {
                isOverText: ds[0].opacity,
                allOp: ds.map(d => d.opacity)
            };
        }''')
        print("Drone opacities:", drone_info)

        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
