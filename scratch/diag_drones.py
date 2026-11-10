import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def diag_drones():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1440, 'height': 900})
        await page.goto('http://localhost:8080/')
        await page.wait_for_timeout(600)
        
        await page.evaluate("""() => {
            const sec = document.getElementById('profile-expertise');
            window.scrollTo({ top: sec.getBoundingClientRect().top + window.scrollY - 80, behavior: 'instant' });
        }""")
        await page.wait_for_timeout(1000)
        
        data = await page.evaluate("""() => {
            const m = window.drones.getMissions().find(m => m.item.id === 'profile-expertise-el-3');
            if (!m) return null;
            return {
                arrived: m.arrivedCount,
                crew: m.crew.map(d => ({
                    id: d.id,
                    isBurst: d.isBurst,
                    state: d.state,
                    flightStart: d.flightStart,
                    flightDuration: d.flightDuration,
                    pathLength: d.pathPoints.length,
                    activeMission: d.activeMission ? d.activeMission.item.id : null
                }))
            };
        }""")
        print("Crew of el-3:", data, flush=True)
        await browser.close()

asyncio.run(diag_drones())
