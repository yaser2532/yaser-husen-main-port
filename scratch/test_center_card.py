import asyncio
from playwright.async_api import async_playwright

async def test_card_build_when_centered():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1440, 'height': 900})
        await page.goto('http://localhost:8080/', wait_until='networkidle')
        
        # Scroll to center the project card in the band
        card = page.locator('.project-card').first
        await card.scroll_into_view_if_needed()
        # Scroll up or down slightly to center it
        await page.evaluate("window.scrollBy(0, 150)")
        
        print("Waiting for drone build...")
        for i in range(25):
            state = await page.evaluate('''() => {
                const c = document.querySelector('.project-card');
                const r = c.getBoundingClientRect();
                const viewH = window.innerHeight;
                const bandTop = viewH * 0.08;
                const bandBottom = viewH * 0.88;
                const vTop = Math.max(r.top, bandTop);
                const vBottom = Math.min(r.bottom, bandBottom);
                const vHeight = Math.max(0, vBottom - vTop);
                const percent = (vHeight / r.height * 100).toFixed(1);
                return {
                    i: percent + '% in band',
                    state: c.getAttribute('data-drone-state'),
                    opacity: window.getComputedStyle(c).opacity,
                    activeMissions: window.__droneActiveMissions || 0
                };
            }''')
            print(f"[{i*0.3:.1f}s]", state)
            if state['state'] == 'built':
                print("BUILT SUCCESS!")
                break
            await asyncio.sleep(0.3)
            
        await browser.close()

if __name__ == '__main__':
    asyncio.run(test_card_build_when_centered())
