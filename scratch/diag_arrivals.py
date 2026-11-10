import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def diag_arrivals():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1440, 'height': 900})
        await page.goto('http://localhost:8080/')
        await page.wait_for_timeout(600)
        
        await page.evaluate("""() => {
            const sec = document.getElementById('profile-expertise');
            window.scrollTo({ top: sec.getBoundingClientRect().top + window.scrollY - 80, behavior: 'instant' });
        }""")
        
        for t in range(0, 1600, 200):
            await page.wait_for_timeout(200)
            data = await page.evaluate("""() => {
                const missions = window.drones.getMissions();
                return missions.map(m => ({
                    id: m.item.id,
                    state: m.item.state,
                    arrived: m.arrivedCount,
                    crewTotal: m.crew.length,
                    crewStates: m.crew.map(d => ({ id: d.id, isBurst: d.isBurst, state: d.state })),
                    elapsed: performance.now() - m.dispatchedAt
                }));
            }""")
            print(f"--- T={t+200}ms ---", flush=True)
            for m in data:
                print(f"  {m['id']}: state={m['state']}, arrived={m['arrived']}/{m['crewTotal']}, elapsed={m['elapsed']:.1f}ms", flush=True)
                
        await browser.close()

asyncio.run(diag_arrivals())
