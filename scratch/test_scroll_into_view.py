import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def test_scroll_into_view():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1440, 'height': 900})
        await page.goto('http://localhost:8080/')
        await page.wait_for_timeout(600)
        
        print("Scrolling into view of profile-expertise...", flush=True)
        await page.evaluate("""() => {
            const sec = document.getElementById('profile-expertise');
            sec.scrollIntoView({ behavior: 'instant', block: 'start' });
        }""")
        
        for t in range(0, 1500, 150):
            await page.wait_for_timeout(150)
            data = await page.evaluate("""() => {
                const missions = window.drones.getMissions();
                const els = window.drones.getElements().filter(e => e.secId === 'profile-expertise');
                return {
                    scrollY: window.scrollY,
                    dwellMet: els[0]?.secInfo?.dwellMet,
                    missionsCount: missions.length,
                    missionStates: missions.map(m => ({ item: m.item.id, state: m.item.state, elapsed: performance.now() - m.dispatchedAt })),
                    elStates: els.map(e => ({ id: e.id, state: e.state }))
                };
            }""")
            print(f"T={t+150}ms: missions={data['missionsCount']}, dwell={data['dwellMet']}, states={data['elStates'][:4]}", flush=True)
            
        await browser.close()

asyncio.run(test_scroll_into_view())
