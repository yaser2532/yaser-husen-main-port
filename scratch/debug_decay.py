import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        page = await b.new_page(viewport={'width': 1440, 'height': 900})
        await page.goto('http://localhost:8080/')
        await page.wait_for_timeout(500)

        # Move mouse to (720, 450)
        await page.mouse.move(720, 450)
        print("Moved mouse to (720, 450), tracking over next 600ms:")

        for i in range(12):
            await page.wait_for_timeout(50)
            res = await page.evaluate('''() => {
                const ds = window.drones.getDrones();
                return {
                    trail0: ds[0].trail.length,
                    alpha0: ds[0].tailAlpha.toFixed(3),
                    speed0: Math.hypot(ds[0].vx, ds[0].vy).toFixed(2),
                    reloc0: ds[0].isRelocating
                };
            }''')
            print(f"t={i*50}ms: trail={res['trail0']} alpha={res['alpha0']} speed={res['speed0']} reloc={res['reloc0']}")
        await b.close()

if __name__ == '__main__':
    asyncio.run(main())
