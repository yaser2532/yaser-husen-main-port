import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def run_v1():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1440, 'height': 900})
        await page.goto('http://localhost:8080/', wait_until='networkidle')
        await page.wait_for_timeout(600)
        
        print("Testing V1: Scroll to profile-expertise and track states...", flush=True)
        await page.evaluate("""() => {
            const sec = document.getElementById('profile-expertise');
            window.scrollTo({ top: sec.offsetTop + 10, behavior: 'instant' });
        }""")
        
        for t in range(0, 1200, 100):
            await page.wait_for_timeout(100)
            metrics = await page.evaluate("""() => {
                const els = window.drones.getElements().filter(e => e.secId === 'profile-expertise');
                const missions = window.drones.getMissions();
                return {
                    states: els.map(e => e.state),
                    missions: missions.length,
                    activeDrones: window.drones.getDrones().map(d => d.state)
                };
            }""")
            print(f"T={t+100}ms: missions={metrics['missions']}, states={metrics['states'][:4]}", flush=True)
            
        await browser.close()

asyncio.run(run_v1())
