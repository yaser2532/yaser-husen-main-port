import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1440, "height": 900})
        await page.goto("http://localhost:8080/")
        await page.wait_for_timeout(1000)
        
        info = await page.evaluate('''() => {
            // Get element stats from drone system
            const elements = window.__droneElementList || [];
            // Let's inspect all elements with [data-drone-state]
            const allDroneEls = Array.from(document.querySelectorAll('[data-drone-state]'));
            const stateCounts = {};
            allDroneEls.forEach(el => {
                const s = el.getAttribute('data-drone-state');
                stateCounts[s] = (stateCounts[s] || 0) + 1;
            });
            return {
                totalMarked: allDroneEls.length,
                states: stateCounts,
                sample: allDroneEls.slice(0, 10).map(el => ({ tag: el.tagName, cls: el.className, state: el.getAttribute('data-drone-state') }))
            };
        }''')
        print("Drone Elements at initial load:", info)
        
        # Now scroll through the page
        for i in range(10):
            await page.mouse.wheel(0, 300)
            await page.wait_for_timeout(200)
            
        info_after = await page.evaluate('''() => {
            const allDroneEls = Array.from(document.querySelectorAll('[data-drone-state]'));
            const stateCounts = {};
            allDroneEls.forEach(el => {
                const s = el.getAttribute('data-drone-state');
                stateCounts[s] = (stateCounts[s] || 0) + 1;
            });
            return {
                totalMarked: allDroneEls.length,
                states: stateCounts
            };
        }''')
        print("Drone Elements after scroll:", info_after)
        await browser.close()

asyncio.run(main())
