import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        page = await b.new_page(viewport={'width': 1440, 'height': 900})
        await page.goto('http://localhost:8080/')
        await page.wait_for_timeout(500)
        h1 = await page.query_selector('.hero-title')
        box = await h1.bounding_box()
        print('box:', box)
        await page.mouse.move(box['x'] + 50, box['y'] + box['height'] / 2)
        for i in range(10):
            await page.wait_for_timeout(100)
            dim_op = await page.evaluate('''() => {
                const ds = window.drones.getDrones();
                return {
                    avg: (ds.map(d => d.opacity).reduce((a, b) => a + b, 0) / ds.length).toFixed(3),
                    states: Array.from(new Set(ds.map(d => d.state)))
                };
            }''')
            print(f"step {i}: avg={dim_op['avg']} states={dim_op['states']}")
        await b.close()

if __name__ == '__main__':
    asyncio.run(main())
