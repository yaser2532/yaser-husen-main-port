import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        page = await b.new_page(viewport={'width': 1440, 'height': 900})
        await page.goto('http://localhost:8080/')
        await page.wait_for_timeout(500)
        await page.evaluate("document.getElementById('about-me').scrollIntoView()")
        for t in [400, 800, 1200, 1600, 2000]:
            await page.wait_for_timeout(400)
            state = await page.evaluate('''() => {
                const cb = document.querySelector('.code-block-visual');
                return {
                    droneState: cb.getAttribute('data-drone-state'),
                    opacity: window.getComputedStyle(cb).opacity
                };
            }''')
            print(f"t={t}ms: state={state['droneState']} opacity={state['opacity']}")
        await b.close()

if __name__ == '__main__':
    asyncio.run(main())
