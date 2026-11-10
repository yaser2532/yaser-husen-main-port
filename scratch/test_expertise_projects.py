import asyncio
import time
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1440, 'height': 900})
        await page.goto('http://localhost:8080/', wait_until='networkidle')

        # Scroll into profile-expertise section
        print('\n--- TESTING PROFILE-EXPERTISE SECTION ---')
        await page.evaluate('''() => {
            const sec = document.getElementById('profile-expertise');
            const r = sec.getBoundingClientRect();
            window.scrollTo({ top: window.scrollY + r.top - 60, behavior: 'instant' });
        }''')
        await asyncio.sleep(0.15)

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
            await asyncio.sleep(0.025)

        print(f'Max active missions in profile-expertise: {max_active}')
        assert max_active <= 1, f"Expected max 1 active mission, got {max_active}"

        # Scroll into Projects section
        print('\n--- TESTING PROJECTS SECTION ---')
        await page.evaluate('''() => {
            const sec = document.getElementById('projects');
            const r = sec.getBoundingClientRect();
            window.scrollTo({ top: window.scrollY + r.top - 60, behavior: 'instant' });
        }''')
        await asyncio.sleep(0.15)

        t1 = time.time()
        while time.time() - t1 < 6.0:
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
            await asyncio.sleep(0.025)

        print(f'Max active missions overall: {max_active}')
        assert max_active <= 1, f"Expected max 1 active mission overall, got {max_active}"

        await page.screenshot(path="scratch/expertise_projects_verified.png")
        print("\nScreenshot saved to scratch/expertise_projects_verified.png")
        print("ALL SECTIONS VERIFIED STRICTLY SEQUENTIAL (MAX ACTIVE <= 1)!")
        await browser.close()

if __name__ == '__main__':
    asyncio.run(run())
