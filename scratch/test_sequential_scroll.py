import asyncio
import time
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1440, 'height': 900})
        await page.goto('http://localhost:8080/', wait_until='networkidle')

        # Scroll so about-me top is at 100px
        await page.evaluate('''() => {
            const sec = document.getElementById('about-me');
            const r = sec.getBoundingClientRect();
            window.scrollTo({ top: window.scrollY + r.top - 80, behavior: 'instant' });
        }''')
        await asyncio.sleep(0.2)

        print('Monitoring top elements of about-me...')
        t0 = time.time()
        last_item = None
        max_active = 0
        while time.time() - t0 < 6.0:
            data = await page.evaluate('''() => {
                const missions = window.drones.getMissions();
                return {
                    count: missions.length,
                    item: missions.length ? missions[0].item.id : null,
                    type: missions.length ? missions[0].item.type : null
                };
            }''')
            if data['count'] > max_active:
                max_active = data['count']
            if data['item'] != last_item:
                print(f"  t={round((time.time()-t0)*1000)}ms: mission item: {data['item']} ({data['type']})")
                last_item = data['item']
            await asyncio.sleep(0.03)

        print(f'Max active missions during part 1: {max_active}')
        
        # Now scroll down 280px to bring the cards and code card fully into the band
        print('\nScrolling down 280px to bring cards and code block into band...')
        await page.evaluate('window.scrollBy({ top: 280, behavior: "instant" })')
        await asyncio.sleep(0.2)

        t1 = time.time()
        while time.time() - t1 < 7.0:
            data = await page.evaluate('''() => {
                const missions = window.drones.getMissions();
                return {
                    count: missions.length,
                    item: missions.length ? missions[0].item.id : null,
                    type: missions.length ? missions[0].item.type : null
                };
            }''')
            if data['count'] > max_active:
                max_active = data['count']
            if data['item'] != last_item:
                print(f"  t={round((time.time()-t1)*1000)}ms: mission item: {data['item']} ({data['type']})")
                last_item = data['item']
            await asyncio.sleep(0.03)

        print(f'Max active missions overall: {max_active}')

        # Check final states
        states = await page.evaluate('''() => {
            return window.drones.getElements()
                .filter(e => e.secId === 'about-me')
                .map(e => ({ id: e.id, type: e.type, state: e.state }));
        }''')
        print('\nFinal element states in about-me:')
        for s in states:
            print(f"  {s['id']} ({s['type']}): {s['state']}")

        await page.screenshot(path="scratch/about_me_fully_built.png")
        print("\nScreenshot saved to scratch/about_me_fully_built.png")
        await browser.close()

if __name__ == '__main__':
    asyncio.run(run())
